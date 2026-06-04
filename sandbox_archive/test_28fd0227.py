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

    def matrix_rank(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(min(m, n)):
            if abs(A[i][i]) > 1e-9:
                rank += 1
        return rank

    def algebraic_K_theory(G):
        # Simplified version of computing K_0(G) for an abelian group G
        # This is a placeholder and should be replaced with actual computation
        return len(G)

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_K0_over_r = 0
        
        while instances_tested < 30:
            A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
            rank = matrix_rank(A)
            if rank == 0:
                continue
            
            G = set()
            for i in range(n):
                for j in range(i+1, n):
                    if A[i][j] != A[j][i]:
                        continue
                    G.add((i, j))
            
            K0 = algebraic_K_theory(G)
            instances_tested += 1
            total_K0_over_r += K0 / rank
        
        mean_K0_over_r = total_K0_over_r / instances_tested
        results.append({
            "metric_name": "K0_over_r",
            "metric_value": mean_K0_over_r,
            "instances_tested": instances_tested,
            "n_max": n,
            "conjecture_holds": abs(mean_K0_over_r - rank) <= 1.5,
            "counterexample": "" if abs(mean_K0_over_r - rank) <= 1.5 else f"K0/G = {mean_K0_over_r}, r = {rank}"
        })
    
    return results

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.extend(trial_result)
    
    mean_K0_over_r = sum(r["metric_value"] for r in results) / len(results)
    std_K0_over_r = math.sqrt(sum((r["metric_value"] - mean_K0_over_r) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_K0_over_r} std={std_K0_over_r} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(abs(r["metric_value"] - r["instances_tested"]) > 1.5 for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"K0/G exceeds rank by more than 1.5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")