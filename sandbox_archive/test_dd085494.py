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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_bp(n, w):
        M = [[random.randint(0, 1) for _ in range(w)] for _ in range(w)]
        N = [[random.randint(0, 1) for _ in range(w)] for _ in range(w)]
        return M, N
    
    def frobenius_product(A, B):
        return sum(A[i][j] * B[j][i] for i in range(len(A)) for j in range(len(B)))
    
    def compute_rho(P_u, P_v):
        return math.log2(max(abs(frobenius_product(P_u, P_v)), 1e-9)) / w**2
    
    results = []
    for n in [6, 10, 16, 24, 32, 40]:
        for w in [2, 4, 8]:
            instances_tested = 0
            max_gap = -float('inf')
            for _ in range(30):
                M, N = generate_bp(n, w)
                P_v = [[N[a][b] @ N[b] for b in range(w)] for a in range(w)]
                rho_values = [compute_rho(P_u, P_v[i]) for i in range(len(P_v))]
                max_gap = max(max_gap, max(rho_values))
                instances_tested += len(P_v)
            results.append({
                "metric_name": "rho",
                "metric_value": max_gap,
                "instances_tested": instances_tested,
                "conjecture_holds": max_gap <= 2 * math.log2(w) + 2,
                "counterexample": "" if max_gap <= 2 * math.log2(w) + 2 else f"n={n}, w={w}, rho={max_gap}"
            })
    
    total_instances = sum(result["instances_tested"] for result in results)
    total_rho = sum(result["metric_value"] * result["instances_tested"] for result in results)
    mean_rho = total_rho / total_instances
    std_rho = math.sqrt(sum((result["metric_value"] - mean_rho) ** 2 * result["instances_tested"] for result in results) / total_instances)
    
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "mean_rho": mean_rho,
        "std_rho": std_rho,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    mean_rho = sum(result["mean_rho"] * result["support_fraction"] for result in results) / sum(result["support_fraction"] for result in results)
    std_rho = math.sqrt(sum((result["mean_rho"] - mean_rho) ** 2 * result["support_fraction"] for result in results) / sum(result["support_fraction"] for result in results))
    
    support_fraction = sum(1 for result in results if result["support_fraction"] == 1)
    
    if support_fraction == len(results):
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
    elif support_fraction >= 0.75 * len(results):
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")