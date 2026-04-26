# auto-injected by SEC sandbox
import collections
import json
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
from itertools import combinations, product

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        pivot = A[i][i]
        if pivot == 0:
            return None  # Singular matrix
        for j in range(i + 1, m):
            factor = A[j][i] / pivot
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def matrix_multiplication(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def compute_betti_numbers(A):
    m, n = len(A), len(A[0])
    boundary_matrix = [row[:n] for row in A]
    reduced_matrix = gaussian_elimination(boundary_matrix)
    if reduced_matrix is None:
        return 1
    rank = sum(1 for row in reduced_matrix if any(row))
    return m - rank

def generate_3cnf(n, m):
    variables = list(range(n))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, 2)
        clause.append(random.choice([0, 1]))
        clauses.append(clause)
    return clauses

def is_monotone_formula_size(clauses):
    n = max(abs(var) for var, _, polarity in clauses)
    formula = [False] * (n + 1)
    for clause in clauses:
        var, polarity, _ = clause
        if polarity == 0:
            formula[abs(var)] = True
        else:
            formula[abs(var)] = False
    return all(formula[var] == formula[abs(var)] for var in range(1, n + 1))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 8, 11, 14]
    results = []
    
    for n in n_values:
        m = max(2, n // 3)
        while True:
            clauses = generate_3cnf(n, m)
            if is_monotone_formula_size(clauses):
                break
        
        betti_sum = 0
        for clause_group in combinations(range(m), 2):
            A = [[0] * (m + 1) for _ in range(m + 1)]
            for i in range(m):
                for j in range(m):
                    if i != j and any(clause_group[k] == clause_group[l] for k, l in combinations(range(2), 2)):
                        A[i][j] = 1
            betti_sum += compute_betti_numbers(A)
        
        L_m_f = len(clauses)
        results.append({
            "n": n,
            "m": m,
            "betti_sum": betti_sum,
            "L_m_f": L_m_f,
            "conjecture_holds": betti_sum <= 0.1 * L_m_f
        })
    
    metric_name = "Betti Sum"
    metric_value = sum(result["betti_sum"] for result in results) / len(results)
    instances_tested = sum(result["instances_tested"] for result in results)
    conjecture_holds_all = all(result["conjecture_holds"] for result in results)
    
    if conjecture_holds_all:
        return {
            "metric_name": metric_name,
            "metric_value": metric_value,
            "instances_tested": instances_tested,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        first_failing_seed = seed
        for result in results:
            if not result["conjecture_holds"]:
                first_failing_seed = seed
                break
        
        return {
            "metric_name": metric_name,
            "metric_value": metric_value,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": f"First failing seed: {first_failing_seed}"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed: {first_failing_seed}\"")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")