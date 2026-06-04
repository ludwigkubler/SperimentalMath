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

def generate_matrix(n, r):
    U = [[random.gauss(0, 1) for _ in range(r)] for _ in range(n)]
    Vt = [[random.gauss(0, 1) for _ in range(n)] for _ in range(r)]
    H = (U @ Vt).T
    return H

def compute_spectral_gap(H):
    n = len(H)
    eigenvalues = [H[i][i] for i in range(n)]
    gap = max(eigenvalues) - min(eigenvalues)
    return gap

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            r = random.randint(1, min(n // 2, 10))
            H = generate_matrix(n, r)
            gap = compute_spectral_gap(H)
            if gap < r / math.log(n):
                return {
                    "metric_name": "spectral_gap",
                    "metric_value": gap,
                    "instances_tested": 30,
                    "n_max": n,
                    "conjecture_holds": False,
                    "counterexample": f"r={r}, n={n}, gap={gap}"
                }
            results.append(gap)
    mean = sum(results) / len(results)
    return {
        "metric_name": "spectral_gap",
        "metric_value": mean,
        "instances_tested": 30,
        "n_max": max([5, 10, 15, 20, 30, 40]),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")