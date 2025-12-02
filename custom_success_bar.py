import pandas as pd
import matplotlib.pyplot as plt

# Your mesh data at 5% noise (from output)
data = {
    'Policy': ['Shortest', 'Hybrid Rule', 'RL (PPO)'],
    'Success Rate': ['0.833 ± 0.041 (95% CI: 0.80–0.86)', '0.917 ± 0.029 (95% CI: 0.89–0.94)', '0.904 ± 0.038 (95% CI: 0.88–0.93)'],
    'Mean Fidelity': ['0.854 ± 0.046', '0.889 ± 0.037', '0.896 ± 0.041'],
    'Average Hops': ['4.0 ± 0.0', '4.0 ± 0.5', '3.2 ± 1.1'],
    'Most Common Path': ['N1-N2-N3-N6-N9 (100%)', 'N1-N4-N7-N8-N9 (70%)', 'Mixed (40% diagonal)']
}
df = pd.DataFrame(data)

fig, ax = plt.subplots(figsize=(12, 5))
ax.axis('tight')
ax.axis('off')
table = ax.table(cellText=df.values, colLabels=df.columns, rowLabels=df.index + 1, cellLoc='center', loc='center')
table.auto_set_font_size(False)
table.set_fontsize(12)
table.scale(1.2, 1.5)
plt.title('Mesh Results at 5% Noise (810 Episodes)', fontsize=16)
plt.savefig('custom_results_table.png', dpi=300, bbox_inches='tight')
plt.show()