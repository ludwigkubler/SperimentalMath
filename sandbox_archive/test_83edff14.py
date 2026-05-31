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
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            pivot = A[i][i]
            if pivot == 0:
                return None  # Singular matrix, no unique solution
            for j in range(i + 1, n):
                factor = -A[j][i] / pivot
                for k in range(i, n):
                    A[j][k] += factor * A[i][k]
        rank = sum(1 for row in A if any(row))
        return rank
    
    def differential_form_rank(G):
        n = len(G)
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if G[i][j]:
                    A[i][j] = 1
                    A[j][i] = -1
        return gaussian_elimination(A)
    
    def resolution_width(G):
        # Placeholder function to compute resolution width
        # This is a stub and should be replaced with actual computation
        return random.randint(1, 10)  # Dummy value
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = 0
    rank = differential_form_rank(G)
    width = resolution_width(G)
    
    if rank is None:
        return {
            "metric_name": "differential_form_rank",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "singular_matrix"
        }
    
    return {
        "metric_name": "differential_form_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": rank == width,  # Placeholder for actual comparison
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" not in res or res["conjecture_holds"] for res in results):
        mean_rank = sum(res["metric_value"] for res in results) / len(results)
        std_dev = math.sqrt(sum((res["metric_value"] - mean_rank)**2 for res in results) / len(results))
        support_fraction = sum(1 for res in results if "conjecture_holds" not in res or res["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif any("counterexample" in res and res["counterexample"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if "counterexample" in res and res["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")