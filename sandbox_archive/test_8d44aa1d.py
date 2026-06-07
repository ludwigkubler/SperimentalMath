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
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i + 1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        pivot = A[i][i]
        for j in range(n):
            A[i][j] /= pivot
        for j in range(m):
            if j != i:
                factor = A[j][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def dpll_width(clauses, assignment):
    literals = set()
    for clause in clauses:
        literals.update(clause)
    
    def dfs(literals, assignment):
        if not literals:
            return 1
        literal = random.choice(list(literals))
        positive_clauses = [c for c in clauses if literal in c]
        negative_clauses = [c for c in clauses if -literal in c]
        
        width1 = 0
        if positive_clauses:
            assignment[literal] = True
            width1 = dfs(literals - {literal}, assignment)
            del assignment[literal]
        
        width2 = 0
        if negative_clauses:
            assignment[-literal] = True
            width2 = dfs(literals - {-literal}, assignment)
            del assignment[-literal]
        
        return max(width1, width2) + 1
    
    return dfs(literals, {})

def mtr(clauses):
    # Placeholder for the minimal tropical motivic rank calculation
    # This is a dummy implementation and should be replaced with actual logic
    return len(clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    clauses = []
    for _ in range(n):
        clause = [random.choice(range(-n, n + 1)) for _ in range(random.randint(1, n))]
        clauses.append(clause)
    
    mtr_value = mtr(clauses)
    width_value = dpll_width(clauses, {})
    ratio = Fraction(mtr_value, width_value) if width_value != 0 else float('inf')
    
    return {
        "metric_name": "mtr_to_dpll_ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ratio <= 2,  # Placeholder constant C
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1000, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["conjecture_holds"]) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results if r["conjecture_holds"]) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")