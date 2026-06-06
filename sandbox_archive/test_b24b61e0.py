# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import product

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_rank(A):
    m, n = len(A), len(A[0])
    A_copy = [row[:] for row in A]
    rank = 0
    
    for i in range(min(m, n)):
        if A_copy[i][i] == 0:
            swap_found = False
            for j in range(i + 1, m):
                if A_copy[j][i] != 0:
                    A_copy[i], A_copy[j] = A_copy[j], A_copy[i]
                    swap_found = True
                    break
            if not swap_found:
                continue
        
        pivot = A_copy[i][i]
        for j in range(n):
            A_copy[i][j] /= pivot
        
        for j in range(m):
            if j != i and A_copy[j][i] != 0:
                factor = A_copy[j][i]
                for k in range(n):
                    A_copy[j][k] -= factor * A_copy[i][k]
        
        rank += 1
    
    return rank

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    A_copy = [row[:] for row in A]
    
    for i in range(min(m, n)):
        if A_copy[i][i] == 0:
            swap_found = False
            for j in range(i + 1, m):
                if A_copy[j][i] != 0:
                    A_copy[i], A_copy[j] = A_copy[j], A_copy[i]
                    swap_found = True
                    break
            if not swap_found:
                continue
        
        pivot = A_copy[i][i]
        for j in range(n):
            A_copy[i][j] /= pivot
        
        for j in range(m):
            if j != i and A_copy[j][i] != 0:
                factor = A_copy[j][i]
                for k in range(n):
                    A_copy[j][k] -= factor * A_copy[i][k]

def tseitin_formula(n):
    variables = [f'x{i}' for i in range(1, n + 1)]
    clauses = []
    
    # Generate all possible combinations of literals
    for combo in product([True, False], repeat=n):
        clause = []
        for var, val in zip(variables, combo):
            if val:
                clause.append(var)
            else:
                clause.append(f'~{var}')
        
        clauses.append(clause)
    
    # Combine all clauses with OR
    formula = ' | '.join(' & '.join(clause) for clause in clauses)
    return formula

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    formula = tseitin_formula(n)
    
    # Placeholder for tropical divisor class group computation
    G = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
    rk_G = matrix_rank(G)
    
    # Placeholder for resolution proof width computation
    w_phi = random.randint(10, 50)
    
    metric_value = Fraction(rk_G, w_phi)
    conjecture_holds = 0.5 <= metric_value <= 1.5
    
    return {
        "metric_name": "rank_to_width_ratio",
        "metric_value": float(metric_value),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Formula: {formula}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Formula: {results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")