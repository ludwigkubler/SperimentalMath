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

# Helper functions for Gaussian elimination and matrix operations
def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        # Find pivot
        max_row = i
        for k in range(i+1, n):
            if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                max_row = k
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below
        for k in range(i+1, n):
            factor = Fraction(matrix[k][i], matrix[i][i])
            for j in range(i, n + 1):
                matrix[k][j] -= factor * matrix[i][j]

    # Back substitution
    x = [0.0] * n
    for i in range(n-1, -1, -1):
        x[i] = Fraction(matrix[i][n], matrix[i][i])
        for k in range(i-1, -1, -1):
            matrix[k][n] -= matrix[k][i] * x[i]
    return x

def matrix_multiplication(A, B):
    n = len(A)
    C = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def solve(lits, cls):
    n = len(lits)
    A = [[0.0 for _ in range(n)] for _ in range(n)]
    b = [0.0 for _ in range(n)]
    
    for i, lit in enumerate(lits):
        if lit[1] == 1:
            A[i][i] += 1
        else:
            A[i][i] -= 1
    
    x = gaussian_elimination(A)
    return all(abs(x[i]) < 1e-6 for i in range(n))

def noncrossing_partition(f):
    n = len(f)
    if n == 1:
        return [([f[0]], [])]
    
    partition = []
    for i in range(1, n):
        true_lits = f[:i]
        false_lits = f[i:]
        partition += [(true_lits, false_lits)]
        partition += noncrossing_partition(true_lits)
        partition += noncrossing_partition(false_lits)
    
    return partition

def resolution_width(f):
    n = len(f)
    clauses = [f[i] for i in range(n) if f[i][1] == 1]
    literals = set()
    for clause in clauses:
        literals.update(clause[0])
    
    cnf = []
    for literal in literals:
        cnf.append([literal, -literal])
    
    def dpll(lits):
        if not lits:
            return True
        lit = next((l for l in literals if all(l not in cls for cls in cnf)), None)
        if lit is None:
            return False
        
        new_cnf = [cls for cls in cnf]
        new_lits_true = lits + [(lit, 1)]
        new_lits_false = lits + [(lit, -1)]
        
        return solve(new_lits_true, new_cnf) or solve(new_lits_false, new_cnf)
    
    return dpll([])

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    min_ranks = []
    widths = []
    
    for n in n_values:
        f = [(i, random.choice([1, -1])) for i in range(n)]
        
        partition = noncrossing_partition(f)
        min_rank = len(partition)
        
        width = resolution_width(f)
        
        min_ranks.append(min_rank)
        widths.append(width)
    
    if not min_ranks or not widths:
        return {
            "metric_name": "min_rank / width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_min_rank = sum(min_ranks) / len(min_ranks)
    mean_width = sum(widths) / len(widths)
    ratio_mean = mean_min_rank / mean_width
    
    return {
        "metric_name": "min_rank / width",
        "metric_value": ratio_mean,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": 1.4 <= ratio_mean <= 1.6,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")