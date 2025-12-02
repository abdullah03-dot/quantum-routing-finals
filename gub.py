# analyze_mesh.py
import pandas as pd, matplotlib.pyplot as plt, seaborn as sns

df = pd.read_csv("results_mesh9_1620.csv")
df["noise (%)"] = df["noise"].map({0.005:"0.5%", 0.02:"2.0%", 0.05:"5.0%"})

# add to analyze_mesh.py or run separately
print("\nMOST COMMON PATH PER POLICY (5% noise, purify_double)")
print(df.query("noise==0.05 and ec=='purify_double'").groupby("policy")["path_taken"].agg(lambda x: x.mode()[0]))

print("\nSUCCESS RATE BY POLICY & NOISE (purify_double)")
print(df.query("ec=='purify_double'").groupby(["noise (%)","policy"])["success"].mean().unstack().round(3))

sns.set(style="whitegrid", font_scale=1.3)
plt.figure(figsize=(11,6))
sns.barplot(data=df.query("ec=='purify_double'"),
            x="noise (%)", y="success", hue="policy", errorbar="sd", palette="tab10")
plt.title("3×3 Quantum Mesh Routing — Success Rate (F≥0.8)\nDouble Purification, 60 trials/config", pad=20)
plt.ylabel("Success Rate"); plt.ylim(0,1.05)
plt.legend(title="Policy")
plt.tight_layout()
plt.savefig("mesh9_success_comparison.png", dpi=350)
plt.show()

