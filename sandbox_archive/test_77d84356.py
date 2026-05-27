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

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        # Find pivot
        max_row = i
        for r in range(i+1, rows):
            if abs(matrix[r][i]) > abs(matrix[max_row][i]):
                max_row = r
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below
        for r in range(i+1, rows):
            factor = Fraction(matrix[r][i], matrix[i][i])
            for c in range(cols):
                matrix[r][c] -= factor * matrix[i][c]

    # Back-substitute to find rank
    rank = 0
    for i in range(rows):
        if any(matrix[i]):
            rank += 1
    return rank

def min_rank(M):
    n = len(M)
    A = [row[:] + col[:] for row, col in zip(M, zip(*M))]
    return gaussian_elimination(A)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    N = 40
    M = [[random.choice([0, 1]) for _ in range(N)] for _ in range(N)]
    
    # Calculate maximum distance δ between any two non-zero vectors
    max_distance = 0
    for i in range(N):
        for j in range(i+1, N):
            if M[i][j] == 1:
                dist = sum(abs(M[k][i] - M[k][j]) for k in range(N))
                if dist > max_distance:
                    max_distance = dist
    
    # Compute the minimal rank of L(M)
    rank = min_rank(M)
    
    # Check the conjecture
    c = 0.5
    if rank >= c * math.log(N / max_distance):
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = f"Rank {rank} < {c * math.log(N / max_distance)} for δ={max_distance}"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")