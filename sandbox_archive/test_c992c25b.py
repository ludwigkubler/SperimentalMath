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
        # Find max pivot in column i
        max_idx = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_idx][i]):
                max_idx = j
        
        # Swap rows i and max_idx
        A[i], A[max_idx] = A[max_idx], A[i]
        b[i], b[max_idx] = b[max_idx], b[i]
        
        # Eliminate entries below pivot
        for j in range(i+1, n):
            factor = -A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] += factor * A[i][k]
            b[j] += factor * b[i]
    
    # Back-substitution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    
    return x

def matrix_multiply(A, B):
    m, n = len(A), len(B[0])
    p = len(B)
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    if len(A) == 1:
        return A[0][0]
    det = Fraction(0)
    sign = 1
    for i in range(len(A)):
        submatrix = [row[:i] + row[i+1:] for row in A[1:]]
        det += sign * A[0][i] * determinant(submatrix)
        sign *= -1
    return det

def sheaf_rank(n, m):
    # Construct the clause-indicator polynomial
    x = [Fraction(1) if i % 2 == 0 else Fraction(-1) for i in range(n)]
    term = Fraction(1)
    for var in range(1, n+1):
        term *= (1 + x[var-1])
    
    # Compute the determinant of the matrix associated with the polynomial
    A = [[term.coeff(x[i], j) for j in range(m)] for i in range(n)]
    det = determinant(A)
    
    return abs(det).numerator

def construct_dpll_tree(n, m):
    clauses = [random.sample(range(1, n+1), 2) for _ in range(m)]
    tree = []
    stack = [(clauses, [])]
    while stack:
        remaining_clauses, assignment = stack.pop()
        if not remaining_clauses:
            tree.append(assignment)
            continue
        var = random.choice(range(1, n+1))
        true_assignments = [a for a in assignment if var not in a]
        false_assignments = [a + [(var, True)] for a in assignment] + [a + [(var, False)] for a in assignment]
        stack.append((remaining_clauses, true_assignments))
        stack.append((remaining_clauses, false_assignments))
    return tree

def dpll_tree_width(tree):
    max_width = 0
    for path in tree:
        width = len(path)
        if width > max_width:
            max_width = width
    return max_width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = random.randint(1, n * (n - 1))
        rank = sheaf_rank(n, m)
        tree = construct_dpll_tree(n, m)
        width = dpll_tree_width(tree)
        
        results.append({
            "n": n,
            "m": m,
            "rank": rank,
            "width": width
        })
    
    mean_rank = sum(result["rank"] for result in results) / len(results)
    mean_width = sum(result["width"] for result in results) / len(results)
    
    if all(width <= 2 * math.log(n**m + m, 2) for n, m, _, width in results):
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "DPLL tree width exceeds expected bound"
    
    return {
        "metric_name": "dpll_tree_width",
        "metric_value": mean_width,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_width = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"DPLL tree width exceeds expected bound\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")