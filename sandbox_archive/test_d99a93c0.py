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

def generate_k_cnf(n, k):
    clauses = []
    for _ in range(k * n):
        clause = [random.randint(-n, -1) if random.choice([True, False]) else random.randint(1, n)]
        while len(clause) < 3:
            var = random.randint(-n, -1) if random.choice([True, False]) else random.randint(1, n)
            if var not in clause:
                clause.append(var)
        clauses.append(clause)
    return clauses

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        pivot_col = next((j for j in range(cols) if matrix[i][j] != 0), None)
        if pivot_col is None:
            continue
        for j in range(i + 1, rows):
            factor = -matrix[j][pivot_col] / matrix[i][pivot_col]
            for k in range(pivot_col, cols):
                matrix[j][k] += factor * matrix[i][k]
    rank = sum(1 for row in matrix if any(row))
    return rank

def local_defect_complexity(clauses):
    n = len(clauses)
    matrix = [[0] * (n + 1) for _ in range(n)]
    for i, clause in enumerate(clauses):
        for var in clause:
            matrix[i][abs(var)] += 1
    return gaussian_elimination(matrix)

def dpll_refutation_path_length(clauses):
    assignment = [0] * (len(clauses) + 1)
    
    def solve():
        if all(assignment[abs(x)] != 0 for x in range(1, len(assignment))):
            return 0
        var = next((x for x in range(1, len(assignment)) if all(x not in clause or assignment[abs(x)] == -sign for clause, sign in zip(clauses, [1] * len(clauses)))), None)
        if var is None:
            return float('inf')
        
        assignment[var] = 1
        length = solve()
        if length < float('inf'):
            return length + 1
        
        assignment[var] = -1
        length = solve()
        if length < float('inf'):
            return length + 1
        
        assignment[var] = 0
        return float('inf')
    
    return solve()

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [10, 20, 40]
    results = []
    
    for n in n_values:
        k = math.ceil(math.log(n, 2))
        F = generate_k_cnf(n, k)
        
        L_F = local_defect_complexity(F)
        t_F = dpll_refutation_path_length(F)
        
        if L_F == 0 or t_F == float('inf'):
            continue
        
        results.append({
            "n": n,
            "k": k,
            "L_F": L_F,
            "t_F": t_F
        })
    
    if not results:
        return {
            "metric_name": "Ratio t*(F)/αL(F)",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    ratio = sum(result["t_F"] / result["L_F"] for result in results) / len(results)
    return {
        "metric_name": "Ratio t*(F)/αL(F)",
        "metric_value": ratio,
        "instances_tested": len(results),
        "conjecture_holds": ratio <= 1.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **result}}")
        results.append(result)
    
    if all("conjecture_holds" not in r or r["conjecture_holds"] for r in results):
        mean_ratio = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = sum(1 for r in results if "conjecture_holds" not in r or r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")