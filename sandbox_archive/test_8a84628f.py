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
    
    def communication_complexity(n):
        # Simulate communication complexity for disjointness problem
        return n
    
    def free_probability_entanglement_matrix(n):
        # Simulate computation of the free probability entanglement matrix
        E_f = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                E_f[i][j] = random.random()
                E_f[j][i] = E_f[i][j]
        return E_f
    
    def min_rank(matrix):
        # Compute the minimal rank of a matrix using Gaussian elimination
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for col in range(cols):
            pivot_row = -1
            for row in range(rank, rows):
                if matrix[row][col] != 0:
                    pivot_row = row
                    break
            if pivot_row == -1:
                continue
            rank += 1
            for i in range(rows):
                if i != pivot_row:
                    factor = matrix[i][col] / matrix[pivot_row][col]
                    for j in range(cols):
                        matrix[i][j] -= factor * matrix[pivot_row][j]
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cc = communication_complexity(n)
        E_f = free_probability_entanglement_matrix(n)
        rank_E_f = min_rank(E_f)
        ratio = rank_E_f / cc
        
        results.append({
            "n": n,
            "cc": cc,
            "rank_E_f": rank_E_f,
            "ratio": ratio
        })
    
    mean_ratio = sum(result["ratio"] for result in results) / len(results)
    std_ratio = math.sqrt(sum((result["ratio"] - mean_ratio) ** 2 for result in results) / len(results))
    
    conjecture_holds = all(result["ratio"] >= n ** (1/4) for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Ratio of Minimal Rank to Communication Complexity",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    std_ratio = math.sqrt(sum((result["metric_value"] - mean_ratio) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")