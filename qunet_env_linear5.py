# qunet_env_linear5.py
# Physically valid linear 5-node repeater chain with proper state handling
import random
import numpy as np
from typing import List, Dict, Any


class QNetLinear5:
    """
    Correct linear 5-node quantum repeater chain: N1—N2—N3—N4—N5
    Physics-based fidelity model with depolarizing noise + BBPSSW purification
    """

    def __init__(self, seed: int = None):
        self.rng = np.random.RandomState(seed)
        self.nodes = ["N1", "N2", "N3", "N4", "N5"]
        self.adj = {
            "N1": ["N2"], "N2": ["N1", "N3"], "N3": ["N2", "N4"],
            "N4": ["N3", "N5"], "N5": ["N4"]
        }

    def reset(self, src: str, dst: str, noise_level: float, seed: int = None):
        """Full deterministic reset per episode"""
        if seed is not None:
            self.rng = np.random.RandomState(seed)
            random.seed(seed)

        self.src = src
        self.dst = dst
        self.p = noise_level  # depolarizing probability per elementary link

        self.stats = {
            "num_epr_attempts": 0, "num_epr_successes": 0,
            "swaps_attempted": 0, "swaps_successful": 0,
            "purification_rounds": 0, "final_fidelity": 0.0,
            "path_taken": "", "num_hops": 0, "latency_s": 0.0,
            "notes": ""
        }

    def _elementary_link_fidelity(self) -> float:
        """Single elementary link fidelity with stochastic depolarizing noise"""
        F0 = 0.95  # intrinsic hardware fidelity
        if self.rng.random() < self.p:
            # Full depolarization event
            return self.rng.uniform(0.25, 0.5)
        else:
            # Standard depolarizing channel
            return F0 * (1 - self.p) + (1 - F0) * (1/3)

    def _bbpss_w_purify(self, F: float, rounds: int = 1) -> float:
        """BBPSSW purification – analytic formula"""
        for _ in range(rounds):
            if F < 0.5:
                break
            p_succ = F**2 + 2*F*(1-F)/3 + (1-F)**2/3
            F = (F**2 + (1-F)**2/3) / (p_succ + 1e-12)
        return F

    def _entangle_path(self, path: List[str], ec: str) -> Dict[str, Any]:
        """Execute entanglement swapping along the full path – now with independent noise per link"""
        if len(path) < 2:
            return {"final_fidelity": 0.0, "success": False}

        hops = len(path) - 1
        purify_rounds = {"none": 0, "purify_single": 1, "purify_double": 2}[ec]

        # ------------------------------------------------------------------
        # 1. Generate one noisy elementary link per segment (4 links in linear-5)
        # ------------------------------------------------------------------
        F_end_to_end = 1.0
        for _ in range(hops):
            F_seg = self._elementary_link_fidelity()
            F_end_to_end *= F_seg
            self.stats["num_epr_attempts"] += 2 ** purify_rounds   # realistic cost

        # ------------------------------------------------------------------
        # 2. Apply purification on the resulting end-to-end pair
        # ------------------------------------------------------------------
        F_end_to_end = self._bbpss_w_purify(F_end_to_end, purify_rounds)
        self.stats["purification_rounds"] = purify_rounds

        # ------------------------------------------------------------------
        # 3. Entanglement swapping at each intermediate repeater (3 swaps)
        # ------------------------------------------------------------------
        for _ in range(hops - 1):
            # High-quality two-qubit gate for swapping (F_swap ≈ 0.99 typical)
            F_end_to_end = 0.99 * F_end_to_end + 0.01 * (1/3)
            self.stats["swaps_attempted"] += 1
            self.stats["swaps_successful"] += 1

        # ------------------------------------------------------------------
        # 4. Memory decoherence during coordination
        # ------------------------------------------------------------------
        wait_time = 0.001 * hops      # 1 ms per hop (light + signalling)
        T2 = 0.1                      # 100 ms coherence time
        F_end_to_end = 0.5 + (F_end_to_end - 0.5) * np.exp(-wait_time / T2)

        # ------------------------------------------------------------------
        # 5. Record final statistics
        # ------------------------------------------------------------------
        self.stats["final_fidelity"] = float(F_end_to_end)
        self.stats["num_hops"] = hops
        self.stats["path_taken"] = "-".join(path)
        self.stats["latency_s"] = 0.005 * hops + 0.05   # realistic light + gate time
        self.stats["notes"] = "success" if F_end_to_end >= 0.8 else "failed"

        return self.stats.copy()

    def run_episode(self, policy: str, error_correction: str, seed: int = None) -> Dict[str, Any]:
        if seed is not None:
            self.rng = np.random.RandomState(seed)
            random.seed(seed)

        # Fixed path for linear-5 (all policies currently identical – correct baseline)
        path = ["N1", "N2", "N3", "N4", "N5"]
        return self._entangle_path(path, error_correction)