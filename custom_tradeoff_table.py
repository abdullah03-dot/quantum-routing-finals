import pandas as pd
import matplotlib.pyplot as plt

data = {
    'Feature': ['Noise-aware', 'Deterministic', 'Requires training', 'Computes in real time', 'Performance (mesh 5%)', 'Interpretability', 'Deployment complexity'],
    'Shortest Path': ['No', 'Yes', 'No', 'Yes', 'Low (0.833)', 'High', 'Low'],
    'Hybrid Rule': ['Yes', 'Yes', 'No', 'Yes', 'Medium-High (0.917)', 'High', 'Low'],
    'RL (PPO)': ['Yes', 'No', 'Yes (10 min)', 'Yes (inference)', 'High (0.904)', 'Low', 'High']
}
df = pd.DataFrame(data).set_index('Feature')

fig, ax = plt.subplots(figsize=(10, 5))
ax.axis('tight')
ax.axis('off')
table = ax.table(cellText=df.values, colLabels=df.columns, rowLabels=df.index, cellLoc='center', loc='center')
table.auto_set_font_size(False)
table.set_fontsize(12)
table.scale(1.2, 1.2)
plt.title('Policy Trade-Offs', fontsize=16)
plt.savefig('custom_tradeoff_table.png', dpi=300, bbox_inches='tight')
plt.show()