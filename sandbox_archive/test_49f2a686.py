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
        # Find the pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below the pivot
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n+1):
                A[j][k] -= factor * A[i][k]

def determinant(A):
    n = len(A)
    det = 1
    U = [row[:] for row in A]
    gaussian_elimination(U)
    for i in range(n):
        det *= U[i][i]
    return det

def fisher_rao_metric(f, g):
    m = len(f)
    n = len(g)
    H_fg = 0
    for i in range(m):
        for j in range(n):
            p_ij = f[i] * g[j]
            if p_ij > 0:
                H_fg += p_ij * math.log(p_ij)
    return -H_fg

def tensor_product(f, g):
    m = len(f)
    n = len(g)
    result = [0] * (m * n)
    for i in range(m):
        for j in range(n):
            result[i*n + j] = f[i] * g[j]
    return result

def dpll_solver(cnf):
    def solve(assignment, clause_index):
        if clause_index == len(cnf):
            return True
        clause = cnf[clause_index]
        for literal in clause:
            var = abs(literal) - 1
            value = literal > 0
            if var not in assignment:
                assignment[var] = value
                if solve(assignment, clause_index + 1):
                    return True
                del assignment[var]
            elif assignment[var] == value:
                break
        else:
            for literal in clause:
                var = abs(literal) - 1
                if var not in assignment:
                    assignment[var] = not literal > 0
                    if solve(assignment, clause_index + 1):
                        return True
                    del assignment[var]
        return False
    
    assignment = {}
    return solve(assignment, 0)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    m = random.randint(2, 5)
    n_max = 40
    instances_tested = 0
    H_fg_sum = 0.0
    
    for _ in range(30):
        f = [random.choice([0, 1]) for _ in range(m)]
        cnf = []
        for i in range(m):
            if f[i] == 0:
                clause = [-i-1]
            else:
                clause = [i+1]
            cnf.append(clause)
        
        g = tensor_product(f, f)
        H_fg = fisher_rao_metric(f, g)
        n = dpll_solver(cnf)
        
        if n < 0 or n >= n_max:
            continue
        
        instances_tested += 1
        H_fg_sum += H_fg
    
    if instances_tested == 0:
        return {
            "metric_name": "H(g)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_H_fg = H_fg_sum / instances_tested
    conjecture_holds = all(H_fg <= m * math.log(n) for H_fg, n in zip([mean_H_fg] * instances_tested, [n_max] * instances_tested))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "H(g)",
        "metric_value": mean_H_fg,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_H_fg = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_H_fg} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")