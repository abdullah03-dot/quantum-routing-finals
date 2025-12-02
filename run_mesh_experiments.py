# run_mesh_experiments.py
import csv, time, datetime
from pathlib import Path
from qunet_env_mesh9 import QNetMesh9

OUTFILE = "results_mesh9_1620.csv"
NOISE_LEVELS = [0.005, 0.02, 0.05]
POLICIES = ["shortest", "hybrid_rule", "highest_fidelity"]
EC = ["none", "purify_single", "purify_double"]
TRIALS = 60
SEED_BASE = 20251202

def ensure_header(p):
    header = ["run_id","timestamp","noise","ec","policy","seed",
              "path_taken","num_hops","final_fidelity","latency_s","success","wall_time_s"]
    if not p.exists():
        with open(p,"w",newline="",encoding="utf-8-sig") as f:
            csv.writer(f).writerow(header)

def main():
    out = Path(OUTFILE); ensure_header(out)
    total = len(NOISE_LEVELS)*len(EC)*len(POLICIES)*TRIALS
    print(f"Starting {total} mesh episodes...")
    rid = 0
    for noise in NOISE_LEVELS:
        for ec in EC:
            for pol in POLICIES:
                for trial in range(TRIALS):
                    seed = SEED_BASE + rid
                    env = QNetMesh9(seed=seed)
                    env.reset(noise_level=noise, seed=seed)
                    t0 = time.time()
                    res = env.run_episode(pol, ec, seed)
                    wall = time.time()-t0
                    success = 1 if res["final_fidelity"]>=0.8 else 0
                    row = [rid+1, datetime.datetime.utcnow().isoformat(),
                           noise, ec, pol, seed,
                           res["path_taken"], res["num_hops"],
                           res["final_fidelity"], res["latency_s"],
                           success, round(wall,5)]
                    with open(out,"a",newline="",encoding="utf-8-sig") as f:
                        csv.writer(f).writerow(row)
                    rid += 1
                    if rid % 100 == 0: print(f"Progress: {rid}/{total}")
    print("Mesh benchmark complete →", out.resolve())

if __name__ == "__main__":
    main()