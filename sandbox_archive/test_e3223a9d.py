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
    rows = len(A)
    cols = len(A[0])
    A_rref = [row[:] for row in A]
    
    for i in range(rows):
        if A_rref[i][i] == 0:
            for j in range(i + 1, rows):
                if A_rref[j][i] != 0:
                    A_rref[i], A_rref[j] = A_rref[j], A_rref[i]
                    break
            else:
                continue
        pivot = A_rref[i][i]
        for j in range(i, cols):
            A_rref[i][j] /= pivot
        
        for k in range(rows):
            if k != i and A_rref[k][i] != 0:
                factor = A_rref[k][i]
                for j in range(i, cols):
                    A_rref[k][j] -= factor * A_rref[i][j]
    
    return A_rref

def rank_of_matrix(A):
    rows = len(A)
    cols = len(A[0])
    A_rref = gaussian_elimination(A)
    
    rank = 0
    for i in range(rows):
        if any(A_rref[i][j] != 0 for j in range(cols)):
            rank += 1
    
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    M = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        M[i][i] = 1
    
    rank_F = rank_of_matrix(M)
    ratio = rank_F / math.sqrt(n)
    
    return {
        "metric_name": "Rank Ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": abs(ratio - 1) <= 0.1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(res["metric_value"] for res in results) / len(results)
    std_ratio = math.sqrt(sum((res["metric_value"] - mean_ratio) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='not supported by all seeds' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient evidence")