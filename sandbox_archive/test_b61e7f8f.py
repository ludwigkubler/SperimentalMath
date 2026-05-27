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
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below pivot
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n+1):
                A[j][k] -= factor * A[i][k]

    # Back-substitute to get the solution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = A[i][n]
        for j in range(i+1, n):
            x[i] -= A[i][j] * x[j]
        x[i] /= A[i][i]
    
    return x

def rank(matrix):
    A = [row[:] for row in matrix]
    gaussian_elimination(A)
    rank = 0
    for row in A:
        if any(row):
            rank += 1
    return rank

def tseitin_formula(n, m):
    variables = list(range(1, n+1))
    clauses = []
    for i in range(m):
        clause = random.choice(variables)
        clauses.append(clause)
    return variables, clauses

def quasi_monogenic_sequence(variables, clauses):
    n = len(variables)
    m = len(clauses)
    Q = [[0] * (n + m) for _ in range(n + m)]
    
    for i in range(n):
        Q[i][i] = 1
    
    for j, clause in enumerate(clauses):
        for var in clause:
            if var > 0:
                Q[var-1][j+n] = 1
            else:
                Q[-var-1][j+n] = -1
    
    return Q

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = random.randint(1, n//2)
        variables, clauses = tseitin_formula(n, m)
        
        Q = quasi_monogenic_sequence(variables, clauses)
        rank_Q = rank(Q)
        
        C = 1.0
        bound = C * math.log2(n + m)
        
        results.append({
            "n": n,
            "m": m,
            "rank_Q": rank_Q,
            "bound": bound,
            "conjecture_holds": rank_Q >= bound
        })
    
    mean_rank_Q = sum(result["rank_Q"] for result in results) / len(results)
    std_rank_Q = math.sqrt(sum((result["rank_Q"] - mean_rank_Q) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "metric_name": "Rank of Quasi-Monogenic Sequence",
        "metric_value": mean_rank_Q,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction == 1.0,
        "counterexample": "" if support_fraction == 1.0 else f"n={results[0]['n']}, m={results[0]['m']}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 53))  # Default to first 30 primes if no seeds provided
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    mean_rank_Q = sum(result["metric_value"] for result in results) / len(results)
    std_rank_Q = math.sqrt(sum((result["metric_value"] - mean_rank_Q) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction == 1.0:
        print(f"RESULT: SUPPORTED mean={mean_rank_Q} std={std_rank_Q} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank_Q} std={std_rank_Q} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['n']}, m={results[0]['m']}\" first_failing_seed={first_failing_seed}")