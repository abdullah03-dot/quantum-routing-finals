# run_small_experiments_fixed.py
# Correct, reproducible, state-isolated 540-run sweep
import csv
import time
import datetime
from pathlib import Path

from qunet_env_linear5 import QNetLinear5

# ====================== CONFIG ======================
OUTFILE = "results_linear5_correct_540.csv"
TOPOLOGY = "linear_5"
SRC_NODE = "N1"
DST_NODE = "N5"

ERROR_CORRECTIONS = ["none", "purify_single", "purify_double"]
NOISE_LEVELS = [0.005, 0.01, 0.05]
POLICIES = ["shortest", "hybrid_rule", "highest_fidelity"]  # all same path for now
TRIALS_PER_CONFIG = 20
SEED_BASE = 20251201
# ====================================================

def ensure_header(path: Path):
    header = [
        "run_id","timestamp","topology","src_node","dst_node","noise_level",
        "error_correction","policy_name","seed","path_taken","num_hops",
        "num_epr_attempts","purification_rounds","final_fidelity","latency_s",
        "success","wall_time_s","notes"
    ]
    if not path.exists():
        with open(path, "w", newline="") as f:
            csv.writer(f).writerow(header)

def main():
    outpath = Path(OUTFILE)
    ensure_header(outpath)

    run_id = 0
    total = len(ERROR_CORRECTIONS) * len(NOISE_LEVELS) * len(POLICIES) * TRIALS_PER_CONFIG
    print(f"Starting {total} correct episodes...")

    for ec in ERROR_CORRECTIONS:
        for noise in NOISE_LEVELS:
            for policy in POLICIES:
                for trial in range(TRIALS_PER_CONFIG):
                    seed = SEED_BASE + run_id
                    env = QNetLinear5(seed=seed)  # ← NEW INSTANCE + SEED
                    env.reset(src=SRC_NODE, dst=DST_NODE, noise_level=noise, seed=seed)

                    t0 = time.time()
                    result = env.run_episode(policy=policy, error_correction=ec, seed=seed)
                    wall = time.time() - t0

                    success = 1 if result["final_fidelity"] >= 0.8 else 0
                    row = [
                        run_id + 1,
                        datetime.datetime.utcnow().isoformat(),
                        TOPOLOGY, SRC_NODE, DST_NODE, noise,
                        ec, policy, seed,
                        result["path_taken"], result["num_hops"],
                        result["num_epr_attempts"], result["purification_rounds"],
                        round(result["final_fidelity"], 5), result["latency_s"],
                        success, round(wall, 4), result["notes"]
                    ]

                    with open(outpath, "a", newline="") as f:
                        csv.writer(f).writerow(row)

                    run_id += 1
                    if run_id % 50 == 0:
                        print(f"Progress: {run_id}/{total}")

    print(f"Correct results saved to {outpath.resolve()}")

if __name__ == "__main__":
    main()