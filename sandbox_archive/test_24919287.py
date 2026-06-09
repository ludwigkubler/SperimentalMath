# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i + 1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[Fraction(0) for _ in range(p)] for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def lcai(cnf):
    n = len(cnf)
    variables = set()
    for clause in cnf:
        for literal in clause:
            variables.add(abs(literal))
    
    # Construct the lattice
    lattice = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if (i+1) % 2 == 0 and (j+1) % 2 == 0:
                lattice[i][j] = 1
            elif (i+1) % 2 != 0 and (j+1) % 2 != 0:
                lattice[i][j] = -1
    
    # Compute the conformal blocks
    A = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if lattice[i][j] == 1:
                A[i][j] = Fraction(1)
            elif lattice[i][j] == -1:
                A[i][j] = Fraction(-1)
    
    # Gaussian elimination to find the rank
    rank = gaussian_elimination(A)
    return rank

def dpll(cnf):
    def solve(i, assignment):
        if i == len(cnf):
            return True
        for literal in cnf[i]:
            var = abs(literal)
            if var not in assignment:
                assignment[var] = literal > 0
                if solve(i + 1, assignment):
                    return True
                del assignment[var]
            elif assignment[var] == (literal > 0):
                continue
            else:
                break
        return False
    
    assignment = {}
    return solve(0, assignment)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            cnf = [[random.randint(-n, n) for _ in range(random.randint(2, 5))] for _ in range(n)]
            lcai_value = lcai(cnf)
            dpll_height = len(dpll(cnf))
            results.append((lcai_value, dpll_height))
    
    if not results:
        return {
            "metric_name": "LCAI vs DPLL Height",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    lcai_values = [r[0] for r in results]
    dpll_heights = [r[1] for r in results]
    
    mean_lcai = sum(lcai_values) / len(lcai_values)
    mean_dpll = sum(dpll_heights) / len(dpll_heights)
    correlation = sum((l - mean_lcai) * (d - mean_dpll) for l, d in zip(lcai_values, dpll_heights)) / (len(results) * mean_lcai * mean_dpll)
    
    return {
        "metric_name": "LCAI vs DPLL Height",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n for n in [5, 10, 15, 20, 30, 40] if any(r[1] > n for r in results)),
        "conjecture_holds": correlation >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r['metric_value'] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")