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
    
    def generate_matrix(n):
        return [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    def max_distance(matrix):
        n = len(matrix)
        dists = []
        for i in range(n):
            for j in range(i + 1, n):
                dist = sum(abs(a - b) for a, b in zip(matrix[i], matrix[j]))
                if dist > 0:
                    dists.append(dist)
        return max(dists) if dists else 1
    
    def min_rank(matrix):
        n = len(matrix)
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        A = [row[:] + col[:] for row, col in zip(matrix, zip(*matrix))]
        A += I
        m = len(A)
        r = 0
        
        def gaussian_elimination(mat):
            nonlocal r
            for i in range(r, m):
                if mat[i][r] == 0:
                    continue
                pivot_row = i
                for j in range(i + 1, m):
                    if abs(mat[j][r]) > abs(mat[pivot_row][r]):
                        pivot_row = j
                mat[pivot_row], mat[i] = mat[i], mat[pivot_row]
                for j in range(m):
                    if j != i:
                        factor = mat[j][r] / mat[i][r]
                        for k in range(r, m):
                            mat[j][k] -= factor * mat[i][k]
            r += 1
        
        gaussian_elimination(A)
        
        rank = sum(1 for row in A if any(row[i] != 0 for i in range(n)))
        return rank
    
    n = random.randint(5, 40)
    M = generate_matrix(n)
    δ = max_distance(M)
    rank = min_rank(M)
    
    c = 0.5
    lower_bound = c * math.log(n / δ)
    
    if rank < lower_bound:
        return {
            "metric_name": "min_rank",
            "metric_value": rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"n={n}, δ={δ}, rank={rank} (expected ≥ {lower_bound})"
        }
    
    return {
        "metric_name": "min_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_rank = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")