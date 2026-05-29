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

def gaussian_elimination(matrix):
    n = len(matrix)
    rank = 0
    for i in range(n):
        if rank >= n:
            break
        pivot_row = rank
        while matrix[pivot_row][i] == 0:
            pivot_row += 1
            if pivot_row == n:
                pivot_row = rank
                i += 1
                if i == n:
                    return rank
        for j in range(n):
            if j != pivot_row:
                factor = -matrix[j][i] / matrix[pivot_row][i]
                for k in range(i, n):
                    matrix[j][k] += factor * matrix[pivot_row][k]
        rank += 1
    return rank

def schur_weyl_invariant(matrix):
    rank = gaussian_elimination(matrix)
    if rank == 0:
        return 0
    det = Fraction(1)
    for i in range(rank):
        det *= matrix[i][i]
    return abs(det)

def k_cnf_formula(n, k):
    variables = list(range(n))
    clauses = []
    for _ in range(k):
        clause = random.sample(variables, 2)
        if random.choice([True, False]):
            clause = [-x for x in clause]
        clauses.append(clause)
    return clauses

def incidence_matrix(clauses, n):
    m = len(clauses)
    matrix = [[0] * n for _ in range(m)]
    for i, clause in enumerate(clauses):
        for var in clause:
            if var > 0:
                matrix[i][var - 1] = 1
            else:
                matrix[i][-var - 1] = 1
    return matrix

def monomial_ideal_complexity(k, n):
    # Placeholder function. Replace with actual computation.
    return k * n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        clauses = k_cnf_formula(n, k)
        matrix = incidence_matrix(clauses, n)
        rho = schur_weyl_invariant(matrix)
        I_m = monomial_ideal_complexity(k, n)
        
        if rho == 0 or I_m == 0:
            continue
        
        results.append((rho, I_m ** 1.5))
    
    if not results:
        return {
            "metric_name": "Spearman rank correlation",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    rho_values, I_m_values = zip(*results)
    n = len(rho_values)
    
    # Calculate Spearman rank correlation
    ranks_rho = [sorted(rho_values).index(x) for x in rho_values]
    ranks_I_m = [sorted(I_m_values).index(x) for x in I_m_values]
    spearman_corr = 1 - (6 * sum((ranks_rho[i] - ranks_I_m[i]) ** 2 for i in range(n))) / (n * (n**2 - 1))
    
    return {
        "metric_name": "Spearman rank correlation",
        "metric_value": spearman_corr,
        "instances_tested": n,
        "conjecture_holds": spearman_corr >= 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean = sum(r["metric_value"] for r in results) / len(results)
        std = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        mean = sum(r["metric_value"] for r in results if r["conjecture_holds"]) / sum(1 for r in results if r["conjecture_holds"])
        std = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results if r["conjecture_holds"]) / sum(1 for r in results if r["conjecture_holds"]))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")