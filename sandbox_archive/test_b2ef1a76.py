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
    
    n = 40
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    G = [row[:] for row in G]  # Ensure it's a copy to avoid aliasing issues
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def rank(A):
        m, n = len(A), len(A[0])
        r = 0
        for i in range(m):
            if any(A[i][j] != 0 for j in range(n)):
                r += 1
        return r
    
    def eta_invariant(G):
        A = [[G[i][j] - G[j][i] for j in range(len(G))] for i in range(len(G))]
        rank_A = rank(gaussian_elimination(A))
        return rank_A
    
    eta_G = eta_invariant(G)
    r_G = rank(G)
    
    if eta_G is None or r_G is None:
        return {
            "metric_name": "eta_invariant",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "eta_invariant_or_rank_computation_failed"
        }
    
    if eta_G > r_G**2:
        return {
            "metric_name": "eta_invariant",
            "metric_value": eta_G,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"eta(G) = {eta_G}, r(G)^2 = {r_G**2}"
        }
    
    return {
        "metric_name": "eta_invariant",
        "metric_value": eta_G,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [631, 677, 727, 773, 821, 877, 929]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results if res["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results if res["metric_value"] is not None)) / len(results)
    
    support_count = sum(1 for res in results if res["conjecture_holds"])
    support_fraction = support_count / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='eta(G) > r(G)^2' first_failing_seed={first_failing_seed}")