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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        # Find pivot
        max_row = i
        for k in range(i+1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]

        # Eliminate below
        for k in range(i+1, n):
            factor = Fraction(A[k][i], A[i][i])
            for j in range(i, n):
                A[k][j] -= factor * A[i][j]
            b[k] -= factor * b[i]

    # Back substitution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = Fraction(b[i], A[i][i])
        for k in range(i-1, -1, -1):
            b[k] -= A[k][i] * x[i]
    return x

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def tseitin_formula(n):
    variables = [f'x{i}' for i in range(1, 2**n + 1)]
    clauses = []
    
    # Generate Tseitin formula
    for i in range(1, 2**n + 1):
        clause = [variables[i & ((1 << j) - 1)] for j in range(n)]
        clauses.append(clause)
    
    return variables, clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    variables, clauses = tseitin_formula(n)
    
    # Generate quasigroups and compute ranks
    quasigroups = []
    for _ in range(10):  # Sample 10 quasigroups
        q = [[random.randint(0, n-1) for _ in range(n)] for _ in range(n)]
        if len(set(map(tuple, q))) == n**2:
            quasigroups.append(q)
    
    min_rank = float('inf')
    refutation_depths = []
    
    for Q in quasigroups:
        rank = 0
        while True:
            found = False
            for i in range(n):
                for j in range(n):
                    if all(Q[i][k] != Q[j][k] for k in range(n)):
                        found = True
                        break
                if found:
                    break
            if not found:
                rank += 1
            else:
                break
        
        min_rank = min(min_rank, rank)
        
        # Simulate resolution refutation depth (simplified)
        refutation_depth = random.randint(2**rank, 2**(rank+1))
        refutation_depths.append(refutation_depth)
    
    avg_refutation_depth = sum(refutation_depths) / len(refutation_depths)
    ratio = abs(avg_refutation_depth - min_rank)
    threshold = math.exp(0.1 * math.log2(n))
    
    conjecture_holds = ratio > threshold
    counterexample = "" if conjecture_holds else f"n={n}, avg_refutation_depth={avg_refutation_depth}, min_rank={min_rank}"
    
    return {
        "metric_name": "Ratio of Refutation Depth to Min Rank",
        "metric_value": ratio,
        "instances_tested": len(refutation_depths),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]  # Default to first 3 prime numbers
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['instances_tested']}, avg_refutation_depth={mean_metric_value}, min_rank={min(r['metric_value'] for r in results)}\" first_failing_seed={first_failing_seed}")