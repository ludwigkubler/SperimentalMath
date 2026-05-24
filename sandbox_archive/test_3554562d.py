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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below pivot
        if A[i][i] == 0:
            return None  # Singular matrix, no unique solution
        
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    
    # Back substitution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = A[i][-1]
        for j in range(i+1, n):
            x[i] -= A[i][j] * x[j]
        x[i] /= A[i][i]
    
    return x

def hodge_rank(poly):
    # Convert polynomial to matrix
    n = len(poly)
    A = [[0] * (n + 1) for _ in range(n)]
    for i, coeff in enumerate(poly):
        A[i][i] = coeff
    
    rank = 0
    for row in gaussian_elimination(A):
        if row is not None and any(x != 0 for x in row):
            rank += 1
    
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    num_clauses = random.randint(n, min(2*n, 40))
    clauses = [random.sample(range(n), random.randint(1, 4)) for _ in range(num_clauses)]
    
    # Construct clause indicator polynomial
    poly = [0] * (n + 1)
    for clause in clauses:
        term = 1
        for var in clause:
            term *= (-1) ** (random.choice([0, 1]))
        poly[len(clause)] += term
    
    rank = hodge_rank(poly)
    
    c = 2  # Example constant
    threshold = c * math.log(n)
    
    return {
        "metric_name": "Hodge Rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= threshold,
        "counterexample": "" if rank <= threshold else f"Hodge rank {rank} exceeds threshold {threshold}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.99:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Hodge rank exceeds threshold\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")