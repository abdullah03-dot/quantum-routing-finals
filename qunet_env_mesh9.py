# qunet_env_mesh9.py
import numpy as np, random
from typing import List, Dict, Any
from collections import defaultdict

class QNetMesh9:
    def __init__(self, seed: int = None):
        self.rng = np.random.RandomState(seed)
        self.nodes = [f"N{i}" for i in range(1,10)]
        pos = [(i//3, i%3) for i in range(9)]
        self.node_to_pos = dict(zip(self.nodes, pos))
        self.pos_to_node = {v: k for k, v in self.node_to_pos.items()}

        # Full 8-connectivity (including diagonals)
        self.adj = defaultdict(list)
        for node in self.nodes:
            r, c = self.node_to_pos[node]
            for dr, dc in [(0,1),(1,0),(0,-1),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]:
                nr, nc = r+dr, c+dc
                if 0 <= nr < 3 and 0 <= nc < 3:
                    neigh = self.pos_to_node[(nr,nc)]
                    if neigh != node:
                        self.adj[node].append(neigh)

    def reset(self, src="N1", dst="N9", noise_level=0.01, seed=None):
        if seed is not None:
            self.rng = np.random.RandomState(seed)
            random.seed(seed)
        self.src, self.dst, self.p = src, dst, noise_level
        self.link_fid = defaultdict(dict)
        self.stats = {
            "path_taken":"", "num_hops":0, "final_fidelity":0.0,
            "num_epr_attempts":0, "purification_rounds":0,
            "swaps_successful":0, "latency_s":0.0, "notes":""
        }

    def _sample_link(self, u, v):
        key = tuple(sorted([u,v]))
        if key not in self.link_fid:
            F0 = 0.96
            if self.rng.random() < self.p:
                self.link_fid[key] = self.rng.uniform(0.30, 0.55)
            else:
                self.link_fid[key] = F0 * (1-self.p) + (1-F0)/3
        return self.link_fid[key]

    def _purify(self, F, rounds):
        for _ in range(rounds):
            if F < 0.5: break
            p = F**2 + 2*F*(1-F)/3 + (1-F)**2/3
            F = (F**2 + (1-F)**2/3) / (p + 1e-12)
        return F

    def shortest_path_policy(self) -> List[str]:
        return ["N1","N2","N3","N6","N9"]               # 4-hop classic

    def hybrid_rule_policy(self) -> List[str]:
        cur = self.src; path = [cur]; visited = {cur}
        while cur != self.dst:
            candidates = [(n, self._sample_link(cur,n)) for n in self.adj[cur] if n not in visited]
            if not candidates: break
            scores = []
            for n, F in candidates:
                dist = sum(abs(a-b) for a,b in zip(self.node_to_pos[cur], self.node_to_pos[n]))
                scores.append((F**3 / (dist + 0.1), n))     # strong bias toward fidelity
            _, nxt = max(scores)
            path.append(nxt); cur = nxt; visited.add(cur)
        return path

    def highest_fidelity_policy(self) -> List[str]:
        cur = self.src; path = [cur]; visited = {cur}
        while cur != self.dst:
            cands = [n for n in self.adj[cur] if n not in visited]
            if not cands: break
            nxt = max(cands, key=lambda n: self._sample_link(cur,n))
            path.append(nxt); cur = nxt; visited.add(cur)
        return path

    def run_episode(self, policy: str, ec: str, seed=None) -> Dict[str, Any]:
        if seed is not None:
            self.rng = np.random.RandomState(seed)
            random.seed(seed)

        policy_map = {
            "shortest": self.shortest_path_policy,
            "hybrid_rule": self.hybrid_rule_policy,
            "highest_fidelity": self.highest_fidelity_policy
        }
        path = policy_map[policy]()
        hops = len(path)-1
        if hops == 0: return {"final_fidelity":0.0, "notes":"invalid"}

        F = 1.0
        for i in range(hops):
            F *= self._sample_link(path[i], path[i+1])
            self.stats["num_epr_attempts"] += 4

        rounds = {"none":0, "purify_single":1, "purify_double":2}[ec]
        F = self._purify(F, rounds)
        self.stats["purification_rounds"] = rounds

        for _ in range(max(0, hops-1)):
            F = 0.99*F + 0.01/3
            self.stats["swaps_successful"] += 1

        wait = 0.002 * hops
        F = 0.5 + (F-0.5)*np.exp(-wait/0.1)

        success = F >= 0.8
        self.stats.update({
            "path_taken": "-".join(path),
            "num_hops": hops,
            "final_fidelity": round(float(F),5),
            "latency_s": round(0.006*hops + 0.03,4),
            "notes": "success" if success else "failed"
        })
        return self.stats.copy()