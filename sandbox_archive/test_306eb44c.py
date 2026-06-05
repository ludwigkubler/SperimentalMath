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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(1, n+1):
            clause = [f'-{variables[i-1]}', f'{variables[n+i-1]}']
            clauses.append(clause)
            clause = [f'{variables[i-1]}', f'-{variables[n+i-1]}']
            clauses.append(clause)
        for i in range(1, n+1):
            for j in range(i+1, n+1):
                clause = [f'-{variables[i-1]}', f'-{variables[j-1]}', f'{variables[2*n+i+j-2]}']
                clauses.append(clause)
                clause = [f'{variables[i-1]}', f'{variables[j-1]}', f'-{variables[2*n+i+j-2]}']
                clauses.append(clause)
        return variables, clauses
    
    def matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(n):
            if all(matrix[j][i] == 0 for j in range(m)):
                continue
            pivot_row = next(j for j in range(i, m) if matrix[j][i] != 0)
            matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
            for j in range(m):
                if j != i:
                    factor = -matrix[j][i] / matrix[i][i]
                    for k in range(n):
                        matrix[j][k] += factor * matrix[i][k]
            rank += 1
        return rank
    
    def p_adic_k_theory_invariant(matrix):
        m, n = len(matrix), len(matrix[0])
        invariant = 0
        for i in range(m):
            for j in range(n):
                if matrix[i][j] != 0:
                    invariant += abs(Fraction(matrix[i][j]).numerator) * abs(Fraction(matrix[i][j]).denominator)
        return invariant
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        variables, clauses = generate_tseitin_formula(n)
        matrix = [[0] * (2*n) for _ in range(2*n)]
        for clause in clauses:
            for var in clause:
                if var.startswith('-'):
                    i = int(var[1:]) - 1
                    matrix[i][n+i] = 1
                else:
                    i = int(var) - 1
                    matrix[n+i][i] = 1
        
        r = matrix_rank(matrix)
        kappa = p_adic_k_theory_invariant(matrix)
        
        results.append({
            "n": n,
            "r": r,
            "kappa": kappa,
            "conjecture_holds": kappa <= r**2
        })
    
    metric_value = sum(result["kappa"] for result in results) / len(results)
    instances_tested = len(results)
    n_max = max(result["n"] for result in results)
    conjecture_holds_all = all(result["conjecture_holds"] for result in results)
    counterexample = "" if conjecture_holds_all else "mapping_undefined"
    
    return {
        "metric_name": "p-adic K-theory invariant",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds_all,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")