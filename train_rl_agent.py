# train_rl_agent.py
from stable_baselines3 import PPO
from quantum_routing_gym import QuantumRoutingGym
import torch as th

th.manual_seed(42)
env = QuantumRoutingGym(noise_level=0.05, ec="purify_double")

model = PPO(
    "MlpPolicy",
    env,
    verbose=1,
    learning_rate=3e-4,
    n_steps=2048,
    batch_size=256,
    gae_lambda=0.95,
    gamma=0.99,
    device="cuda" if th.cuda.is_available() else "cpu"
)

print("Training RL agent on 5% noise (this takes ~4 minutes)...")
model.learn(total_timesteps=1_000_000)
model.save("ppo_quantum_router_5percent")

# Quick eval
success = 0
for _ in range(500):
    obs, _ = env.reset()
    done = False
    while not done:
        action, _ = model.predict(obs, deterministic=True)
        obs, r, done, _, info = env.step(action)
    success += info.get("final_fidelity", 0) >= 0.8
print(f"RL Agent success rate (500 trials): {success/500:.4f}")