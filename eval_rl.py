# eval_rl.py   ← put this in your folder
from stable_baselines3 import PPO
# The 'QuantumRoutingGym' must be compatible with the Gymnasium API internally.
# Assuming 'quantum_routing_gym' handles the 'gymnasium' import internally or is designed for the new API.
from quantum_routing_gym import QuantumRoutingGym 

env = QuantumRoutingGym(noise_level=0.05, ec="purify_double")
model = PPO.load("ppo_quantum_router_5percent")   # from earlier training

success = 0
for _ in range(500):
    # CHANGED: env.reset() now returns (observation, info)
    obs, _ = env.reset() 
    terminated = False # Initialize terminated flag
    truncated = False  # Initialize truncated flag

    while not (terminated or truncated): # CHANGED: Loop while neither is True
        action, _ = model.predict(obs, deterministic=True)
        
        # CHANGED: env.step() now returns 5 values: obs, reward, terminated, truncated, info
        obs, _, terminated, truncated, info = env.step(action) 
        
    # The original logic used 'done', we combine terminated and truncated here if needed elsewhere, 
    # but the loop condition is updated.
    
    success += info.get("final_fidelity", 0) >= 0.8
    
print(f"PPO success rate (500 trials): {success/500:.4f}")
