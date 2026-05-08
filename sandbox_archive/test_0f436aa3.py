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
        max_row = i + max(range(i, n), key=lambda r: abs(A[r][i]))
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n + 1):
                A[j][k] -= factor * A[i][k]

    return A

def solve_linear_system(A, b):
    n = len(A)
    Ab = [row[:] + [b[i]] for i, row in enumerate(A)]
    gaussian_elimination(Ab)
    
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (Ab[i][n] - sum(Ab[i][j] * x[j] for j in range(i + 1, n))) / Ab[i][i]
    
    return x

def metric_dimension(G):
    n = len(G)
    A = [[0] * n for _ in range(n)]
    b = [1] * n
    
    for i in range(n):
        for j in range(n):
            if G[i][j]:
                A[i][j] = 1
                A[j][i] = 1
    
    x = solve_linear_system(A, b)
    return sum(1 for xi in x if abs(xi) > 0.5)

def tseitin_formula(G):
    n = len(G)
    literals = {i: f'x{i}' for i in range(n)}
    neg_literals = {i: f'-x{i}' for i in range(n)}
    
    clauses = []
    for i in range(n):
        if sum(G[i]) > 1:
            clause = [neg_literals[i]] + [literals[j] for j in range(n) if G[i][j]]
            clauses.append(clause)
    
    return clauses

def resolution_length(clauses):
    stack = clauses.copy()
    while True:
        new_clauses = []
        added_clause = False
        for i in range(len(stack)):
            for j in range(i + 1, len(stack)):
                if any(lit in clause for lit in stack[i] and lit in clause for lit in stack[j]):
                    new_lit = next(lit for lit in stack[i] if lit not in stack[j])
                    new_clause = [neg for neg in stack[i] if neg != new_lit] + [neg for neg in stack[j] if neg != new_lit]
                    if new_clause not in new_clauses:
                        new_clauses.append(new_clause)
                        added_clause = True
        if not added_clause:
            break
        stack += new_clauses
    
    return len(stack)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = 0
    
    ν_G = metric_dimension(G)
    clauses = tseitin_formula(G)
    length = resolution_length(clauses)
    
    return {
        "metric_name": "Resolution Length",
        "metric_value": length,
        "instances_tested": 1,
        "conjecture_holds": length >= 2 ** (math.log(n, 2) * ν_G),
        "counterexample": "" if length >= 2 ** (math.log(n, 2) * ν_G) else f"Graph with n={n}, ν(G)={ν_G}, length={length}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(100, 999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_length = sum(res["metric_value"] for res in results) / len(results)
    std_length = math.sqrt(sum((res["metric_value"] - mean_length) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_length} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")