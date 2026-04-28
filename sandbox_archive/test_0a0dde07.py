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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        pivot = A[i][i]
        if pivot == 0:
            return None
        for j in range(i + 1, m):
            factor = A[j][i] / pivot
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    rank = sum(1 for row in A if any(row))
    return rank

def subword_complexity(s, k):
    n = len(s)
    complexity = set()
    for i in range(n - k + 1):
        complexity.add(s[i:i+k])
    return len(complexity)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for k in [2, 3, 4]:
        for _ in range(100):
            f = [[random.randint(0, 1) for _ in range(k)] for _ in range(k)]
            M = [[f[i][j] if (i & (1 << j)) else 0 for j in range(k)] for i in range(2**k)]
            rank_M = gaussian_elimination(M)
            if rank_M is None:
                return {
                    "metric_name": "rank",
                    "metric_value": float('inf'),
                    "instances_tested": 1,
                    "conjecture_holds": False,
                    "counterexample": "singular_matrix"
                }
            s_f = max(subword_complexity("".join(map(str, row)), k) for row in M)
            if rank_M < s_f:
                return {
                    "metric_name": "rank",
                    "metric_value": float('inf'),
                    "instances_tested": 1,
                    "conjecture_holds": False,
                    "counterexample": f"p_{row}(k) > rk_R(M)"
                }
            results.append((rank_M, s_f))
    mean_rank = sum(rank for rank, _ in results) / len(results)
    mean_s_f = sum(s_f for _, s_f in results) / len(results)
    support_fraction = sum(1 for rank, s_f in results if rank >= s_f) / len(results)
    return {
        "metric_name": "rank",
        "metric_value": mean_rank,
        "instances_tested": 300,
        "conjecture_holds": support_fraction == 1.0,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(res["metric_value"] for res in results) / len(results)
    mean_s_f = sum(res["instances_tested"] * res["metric_value"] for res in results) / sum(res["instances_tested"] for res in results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"p_{row}(k) > rk_R(M)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")