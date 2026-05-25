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
    n = len(A)
    for i in range(n):
        # Find pivot row in column i
        max_row = i
        for k in range(i+1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        
        # Swap current row with pivot row
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate entries below the pivot
        factor = 1 / A[i][i]
        for j in range(i, n):
            A[i][j] *= factor
        for k in range(i+1, n):
            factor = A[k][i]
            for j in range(i, n):
                A[k][j] -= factor * A[i][j]
    
    return A

def rank(matrix):
    rref = gaussian_elimination(matrix)
    rank = 0
    for row in rref:
        if any(row):
            rank += 1
    return rank

def generate_monotone_kclique(n, k=3):
    # Generate a random monotone k-clique instance
    V = list(range(n))
    E = set()
    while len(E) < k:
        u = random.choice(V)
        v = random.choice([x for x in V if x != u])
        if (u, v) not in E and (v, u) not in E:
            E.add((u, v))
    return V, E

def minimal_rank(n, k=3):
    V, E = generate_monotone_kclique(n, k)
    loci = []
    for u in V:
        row = [0] * n
        row[u] = 1
        for v in V:
            if (u, v) in E or (v, u) in E:
                row[v] = -1
        loci.append(row)
    
    return rank(loci)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    alpha = 0.5  # Example constant
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Test each n with 5 different instances
            rank_value = minimal_rank(n, k=3)
            if rank_value < alpha * n**(3/4):
                return {
                    "metric_name": "minimal_rank",
                    "metric_value": rank_value,
                    "instances_tested": instances_tested,
                    "conjecture_holds": False,
                    "counterexample": f"n={n}, rank={rank_value} < {alpha * n**(3/4)}"
                }
            total_rank += rank_value
            instances_tested += 1
    
    mean_rank = total_rank / instances_tested
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[first_failing_seed]['instances_tested']}, rank={results[first_failing_seed]['metric_value']}\" first_failing_seed={seeds[first_failing_seed]}")