# quantum-routing-finals
Master's paper on quantum network routing: linear/mesh simulations, hybrid rule, and RL agent
# Quantum Network Routing Thesis

Master's paper on routing in noisy quantum networks: linear-5 chain, 3x3 mesh, hybrid F³/d rule, and PPO RL agent.

## Quick Start
1. Install dependencies:

conda create -n qrouting_new python=3.11
conda activate qrouting_new
conda install numpy=1.26.4 pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia -y
pip install stable-baselines3[extra]==2.3.2 gymnasium==0.29.1 shimmy tensorboard matplotlib pandas seaborn

2. Setup env:  conda activate qrouting_new

3. Run linear experiments: `python run_small_experiments_fixed.py` (540 episodes, ~30 sec)  

4. Run mesh experiments: `python run_mesh_experiments.py` (1620 episodes, ~3 min)  

5. Analyze mesh: `python analyze_mesh.py` (bar plot + table)  

6. Path visualization: `python plot_paths.py`  

7. RL evaluation: `python eval_rl.py` (500 trials, ~8 sec)  

## Files Overview
- Linear sim: qunet_env_linear5.py, run_small_experiments_fixed.py  
- Mesh sim (final): qunet_env_mesh9.py, run_mesh_experiments.py  
- Mesh variants (early): qunet_env_fullmesh1.py, qunet_env_fullmesh2.py, qunet_env.py  
- RL: quantum_routing_gym.py, train_rl_agent.py, eval_rl.py  
- Analysis/Plots: analyze_mesh.py, plot_paths.py, custom_success_bar.py, custom_route_heatmap.py, custom_fidelity_violin.py, custom_tradeoff_table.py, analyze_results.py, plot_results1.py  
- Original runners: run_small_experiments.py, run_small_experiments1.py  
- Data: results_linear5_correct_540.csv, results_mesh9_1620.csv  

Thesis PDF included.

License: MIT