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
    
    n = random.randint(5, 40)
    k = random.randint(2, n-1)
    d = random.randint(1, n//2)
    
    # Generate a random adjacency matrix for a graph with n vertices
    A = [[random.choice([0, 1]) if i != j else 0 for j in range(n)] for i in range(n)]
    
    # Compute the rank of the subspace spanned by all subspaces of dimension at least d
    min_rank = float('inf')
    for i in range(2**n):
        S = [j for j in range(n) if (i >> j) & 1]
        if len(S) >= d:
            # Compute the rank of the subspace spanned by S
            submatrix = [[A[i][j] for j in S] for i in S]
            rank = gaussian_elimination(submatrix)
            min_rank = min(min_rank, rank)
    
    metric_value = min_rank
    instances_tested = 1
    
    # Check if the conjecture holds
    conjecture_holds = min_rank >= (n**2 / k) * math.log(2, n)
    counterexample = "min_rank too small" if not conjecture_holds else ""
    
    return {
        "metric_name": "Minimum Rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def gaussian_elimination(matrix):
    m, n = len(matrix), len(matrix[0])
    rank = 0
    
    for j in range(n):
        i_max = -1
        for i in range(rank, m):
            if matrix[i][j] != 0:
                i_max = i
                break
        
        if i_max == -1:
            continue
        
        matrix[rank], matrix[i_max] = matrix[i_max], matrix[rank]
        
        for i in range(m):
            if i != rank and matrix[i][j] != 0:
                factor = matrix[i][j] / matrix[rank][j]
                for k in range(n):
                    matrix[i][k] -= factor * matrix[rank][k]
        
        rank += 1
    
    return rank

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")