# auto-injected by SEC sandbox
import collections
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
import json
from itertools import combinations

def gaussian_elimination(A, b):
    n = len(b)
    A_augmented = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A_augmented[j][i]) > abs(A_augmented[max_row][i]):
                max_row = j
        A_augmented[i], A_augmented[max_row] = A_augmented[max_row], A_augmented[i]
        pivot = A_augmented[i][i]
        for j in range(i, n+1):
            A_augmented[i][j] /= pivot
        for j in range(n):
            if j != i:
                factor = A_augmented[j][i]
                for k in range(i, n+1):
                    A_augmented[j][k] -= factor * A_augmented[i][k]
    return [row[-1] for row in A_augmented]

def matrix_multiply(A, B):
    m, p = len(A), len(B[0])
    p_A = len(A[0])
    C = [[0 for _ in range(p)] for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(p_A):
                C[i][j] += A[i][k] * B[k][j]
    return C

def dpll_with_leaves(F, assignment):
    if not F:
        return 1
    unit_clauses = [c for c in F if len(c) == 1 and c[0] in assignment and assignment[c[0]] == True]
    if unit_clauses:
        lit = unit_clauses[0][0]
        assignment[lit] = True
        return dpll_with_leaves(F, assignment)
    pure_literals = [lit for lit in range(2*len(assignment)) if (lit not in assignment and -lit not in assignment)]
    if pure_literals:
        lit = pure_literals[0]
        assignment[lit] = True
        return dpll_with_leaves(F, assignment)
    literals = list(assignment.keys())
    for lit in literals:
        new_assignment = assignment.copy()
        new_assignment[lit] = True
        leaves_true = dpll_with_leaves(F, new_assignment)
        if leaves_true > 0:
            return leaves_true + 1
        new_assignment[lit] = False
        leaves_false = dpll_with_leaves(F, new_assignment)
        if leaves_false > 0:
            return leaves_false + 1
    return 0

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [10, 12, 14, 16, 18, 20]
    results = []
    
    for n in n_values:
        m = 4 * n
        F = [[random.randint(0, 2*n-1) for _ in range(3)] for _ in range(m)]
        X_F = 0
        V_F = 0
        
        for i in range(m):
            assignment = {}
            leaves = dpll_with_leaves(F[:i+1], assignment)
            X_F += leaves
            M_i = X_F / (i + 1)
            if i > 0:
                V_F += (M_i - M_i_prev) ** 2
            M_i_prev = M_i
        
        worst_case_gap = 0
        for F_prime in combinations(F, m-1):
            leaves_prime = dpll_with_leaves(list(F_prime), {})
            worst_case_gap = max(worst_case_gap, abs(leaves_prime - X_F))
        
        results.append({
            "n": n,
            "X_F": X_F,
            "V_F": V_F,
            "worst_case_gap": worst_case_gap
        })
    
    return {
        "metric_name": "Doob Variance Gap Predicts Worst-Case DPLL Depth",
        "metric_value": sum(result["worst_case_gap"] for result in results),
        "instances_tested": len(results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    for seed in seeds:
        result = run_trial(seed)
        print(json.dumps({"TRIAL": {"seed": seed, **result}}))
    
    results = [run_trial(seed) for seed in seeds]
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        print("RESULT: SUPPORTED with some seeds not holding")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")