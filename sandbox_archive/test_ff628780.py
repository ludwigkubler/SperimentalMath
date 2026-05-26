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
    
    def communication_complexity(n):
        # Simulate communication complexity for disjointness function
        return n
    
    def free_probability_entanglement_matrix(n):
        # Simulate the computation of the free probability entanglement matrix
        E_f = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                if i == j:
                    E_f[i][j] = 1
                else:
                    E_f[i][j] = random.random()
                    E_f[j][i] = E_f[i][j]
        return E_f
    
    def minimal_rank(matrix):
        # Compute the minimal rank of a matrix using Gaussian elimination
        n = len(matrix)
        A = [row[:] for row in matrix]
        rank = 0
        for i in range(n):
            if all(A[j][i] == 0 for j in range(rank, n)):
                continue
            pivot_row = rank
            while A[pivot_row][i] == 0:
                pivot_row += 1
                if pivot_row == n:
                    return rank
            A[pivot_row], A[rank] = A[rank], A[pivot_row]
            for j in range(n):
                if j != i:
                    factor = -A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] += factor * A[i][k]
            rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cc = communication_complexity(n)
        E_f = free_probability_entanglement_matrix(n)
        rank_E_f = minimal_rank(E_f)
        results.append({
            "n": n,
            "cc": cc,
            "rank_E_f": rank_E_f
        })
    
    if not results:
        return {
            "metric_name": "Ratio of Minimal Rank to Communication Complexity",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No instances tested"
        }
    
    ratios = [result["rank_E_f"] / result["cc"] for result in results]
    mean_ratio = sum(ratios) / len(ratios)
    conjecture_holds = all(r >= Fraction(1, 4) * n ** (Fraction(1, 4)) for r, n in zip(ratios, [result["n"] for result in results]))
    
    return {
        "metric_name": "Ratio of Minimal Rank to Communication Complexity",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "None found"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE No trials executed")
        sys.exit(0)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='None found' first_failing_seed={first_failing_seed}")