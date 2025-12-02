# quantum_routing_gym.py
import gymnasium as gym
from gymnasium import spaces
import numpy as np
from qunet_env_mesh9 import QNetMesh9

class QuantumRoutingGym(gym.Env):
    metadata = {"render_modes": []}

    def __init__(self, noise_level=0.05, ec="purify_double"):
        super().__init__()
        self.noise = noise_level
        self.ec = ec
        self.base_env = QNetMesh9()

        # Observation: one-hot current node (9) + one-hot target (9) + noise level
        self.observation_space = spaces.Box(low=0, high=1, shape=(19,), dtype=np.float32)
        self.action_space = spaces.Discrete(9)  # 0..8 → N1..N9

        self.current_node = None
        self.target = "N9"
        self.path = []

    # CHANGED: Added 'seed' parameter as per Gymnasium API requirements
    def reset(self, seed=None, options=None):
        # We must set the seed in the base class via super().reset() first
        super().reset(seed=seed) 
        
        # Pass the seed down to your internal environment if it uses numpy.random internally
        # (Assuming QNetMesh9 reset can handle a seed argument, or using self.np_random if needed)
        self.base_env.reset(src="N1", dst="N9", noise_level=self.noise, seed=seed)
        
        self.current_node = "N1"
        self.path = ["N1"]
        
        observation = self._get_obs()
        info = {} # Reset also returns an empty info dict
        return observation, info

    def _get_obs(self):
        obs = np.zeros(19, dtype=np.float32)
        curr_idx = int(self.current_node[1:]) - 1
        obs[curr_idx] = 1.0
        obs[9 + 8] = 1.0  # target N9
        obs[18] = self.noise
        return obs

    # CHANGED: Step must return 5 values: obs, reward, terminated, truncated, info
    def step(self, action):
        next_node = f"N{action + 1}"
        
        # Initialize flags
        terminated = False
        truncated = False
        info = {}
        
        if next_node not in self.base_env.adj[self.current_node]:
            reward = -10.0
            terminated = True # Invalid move terminates the episode
            info["notes"] = "invalid move"
            # Return 5 items: obs, reward, terminated, truncated, info
            return self._get_obs(), reward, terminated, truncated, info

        self.path.append(next_node)
        self.current_node = next_node

        if next_node == self.target:
            # Execute full path logic
            self.base_env.link_fid = {}  # force resample
            F = 1.0
            for i in range(len(self.path)-1):
                F *= self.base_env._sample_link(self.path[i], self.path[i+1])
            F = self.base_env._purify(F, {"purify_double": 2}.get(self.ec, 0))
            for _ in range(max(0, len(self.path)-2)):
                F = 0.99*F + 0.01/3
            F = 0.5 + (F-0.5)*np.exp(-0.002*(len(self.path)-1)/0.1)
            
            success = F >= 0.8
            reward = 10.0 if success else -5.0
            terminated = True # Goal reached terminates the episode
            info = {"final_fidelity": F, "path": "-".join(self.path)}
            
            # Return 5 items: obs, reward, terminated, truncated, info
            return self._get_obs(), reward, terminated, truncated, info
        else:
            reward = -0.1
            # Return 5 items: obs, reward, terminated, truncated, info (not terminated yet)
            return self._get_obs(), reward, terminated, truncated, info 

    def render(self):
        # The render function remains unchanged, as it follows basic Python conventions
        print(f"Path so far: {'-'.join(self.path)}")

