# auto-injected by SEC sandbox
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gromov_hyperbolicity(F):
        n = len(F)
        d = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                d[i][j] = abs(S[i] ^ S[j])
                d[j][i] = d[i][j]
        
        def dist(a, b):
            return d[a][b]
        
        max_delta_star = 0
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    for l in range(k + 1, n):
                        M1 = dist(i, j) + dist(k, l)
                        M2 = dist(i, k) + dist(j, l)
                        M3 = dist(i, l) + dist(j, k)
                        delta_star = (M1 - M2) / (2 * max(dist(x, y) for x in range(n) for y in range(n)))
                        if delta_star > max_delta_star:
                            max_delta_star = delta_star
        return max_delta_star
    
    def generate_clique_dnf(v):
        n = v * (v - 1) // 2
        k = int(math.sqrt(v))
        F_clique = []
        edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
        for clique in itertools.combinations(edges, k):
            S = set()
            for u, v in clique:
                S.add(u)
                S.add(v)
            F_clique.append(S)
        return F_clique
    
    def generate_random_dnf(n, k, num_clauses):
        F_rand = []
        for _ in range(num_clauses):
            S = random.sample(range(n), k)
            F_rand.append(set(S))
        return F_rand
    
    v_values = [8, 10, 12, 14, 16, 18, 20]
    results = []
    
    for v in v_values:
        n = v * (v - 1) // 2
        k = int(math.sqrt(v))
        
        F_clique = generate_clique_dnf(v)
        delta_F_clique = gromov_hyperbolicity(F_clique)
        if delta_F_clique < 0.2:
            return {
                "metric_name": "delta_F_clique",
                "metric_value": delta_F_clique,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": "F_clique has low Gromov hyperbolicity"
            }
        
        mean_delta_F_rand = 0
        for _ in range(30):
            F_rand = generate_random_dnf(n, k, len(F_clique))
            delta_F_rand = gromov_hyperbolicity(F_rand)
            if delta_F_rand >= 0.2:
                return {
                    "metric_name": "delta_F_clique",
                    "metric_value": delta_F_clique,
                    "instances_tested": 1,
                    "conjecture_holds": False,
                    "counterexample": f"F_rand has high Gromov hyperbolicity: {delta_F_rand}"
                }
            mean_delta_F_rand += delta_F_rand
        
        mean_delta_F_rand /= 30
        R_v = delta_F_clique / mean_delta_F_rand
        if R_v < 0.3 * math.sqrt(v) / math.log(v):
            return {
                "metric_name": "delta_F_clique",
                "metric_value": delta_F_clique,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"R_v {R_v} < 0.3 * sqrt({v}) / log({v})"
            }
        
        results.append({
            "metric_name": "delta_F_clique",
            "metric_value": delta_F_clique,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        })
    
    return {
        "metric_name": "delta_F_clique",
        "metric_value": sum(r["metric_value"] for r in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": all(r["conjecture_holds"] for r in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"R_v too low\" first_failing_seed={first_failing_seed}")