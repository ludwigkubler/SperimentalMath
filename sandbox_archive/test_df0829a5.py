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
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        for j in range(i+1, n):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(n):
                matrix[j][k] -= factor * matrix[i][k]
    return matrix

def determinant(matrix):
    n = len(matrix)
    det = 1
    for i in range(n):
        if matrix[i][i] == 0:
            return 0
        det *= matrix[i][i]
        for j in range(i+1, n):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(n):
                matrix[j][k] -= factor * matrix[i][k]
    return det

def minimal_order(clauses):
    variables = set()
    for clause in clauses:
        for literal in clause:
            variables.add(abs(literal))
    n = len(variables)
    
    # Construct the Tseitin formula
    tseitin_count = 0
    tseitin_vars = {}
    for i, var in enumerate(sorted(variables)):
        tseitin_vars[var] = n + i
    
    new_clauses = []
    for clause in clauses:
        if len(clause) == 1:
            new_clauses.append([tseitin_vars[abs(clause[0])]])
        else:
            new_var = n + tseitin_count
            tseitin_count += 1
            new_clauses.append([-new_var])
            for literal in clause:
                new_clauses.append([new_var, literal])
    
    # Construct the matrix for Gaussian elimination
    matrix = []
    for i in range(n):
        row = [0] * n
        row[i] = 1
        matrix.append(row)
    
    for clause in new_clauses:
        if len(clause) == 2:
            var1, var2 = abs(clause[0]), abs(clause[1])
            matrix[tseitin_vars[var1]-n][tseitin_vars[var2]-n] = -1
            matrix[tseitin_vars[var2]-n][tseitin_vars[var1]-n] = -1
    
    # Perform Gaussian elimination and calculate the determinant
    det = determinant(gaussian_elimination(matrix))
    
    return abs(det)

def monotone_width(clauses):
    n = len(set(abs(literal) for clause in clauses for literal in clause))
    max_depth = 0
    stack = []
    for i, clause in enumerate(clauses):
        if len(clause) == 1:
            continue
        depth = 1
        for literal in clause:
            if literal > 0 and literal not in stack:
                stack.append(literal)
                depth += 1
        max_depth = max(max_depth, depth)
        while stack and stack[-1] != abs(clause[0]):
            stack.pop()
    return max_depth

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        instances_tested = 0
        m_Cphi_sum = 0
        w_Cphi_sum = 0
        for _ in range(5):  # Sample 5 random instances per size
            clauses = []
            for _ in range(n):
                literals = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
                if random.random() < 0.5:
                    literals.append(random.choice([-1, 1]) * (n + 1))
                clauses.append(literals)
            m_Cphi = minimal_order(clauses)
            w_Cphi = monotone_width(clauses)
            instances_tested += 1
            m_Cphi_sum += m_Cphi
            w_Cphi_sum += w_Cphi
        mean_m_Cphi = m_Cphi_sum / instances_tested
        mean_w_Cphi = w_Cphi_sum / instances_tested
        
        results.append({
            "n": n,
            "mean_m_Cphi": mean_m_Cphi,
            "mean_w_Cphi": mean_w_Cphi,
            "instances_tested": instances_tested
        })
    
    m_Cphi_total = sum(result["mean_m_Cphi"] for result in results)
    w_Cphi_total = sum(result["mean_w_Cphi"] for result in results)
    k = m_Cphi_total / w_Cphi_total
    
    conjecture_holds = True
    counterexample = ""
    for result in results:
        if result["instances_tested"] > 0 and result["n"] <= 40:
            m_Cphi = result["mean_m_Cphi"]
            w_Cphi = result["mean_w_Cphi"]
            if m_Cphi >= k * w_Cphi:
                conjecture_holds = False
                counterexample = f"m(Cφ)={m_Cphi} is not less than k*w(Cφ)={k*w_Cphi}"
    
    return {
        "metric_name": "min_order_over_monotone_width",
        "metric_value": k,
        "instances_tested": sum(result["instances_tested"] for result in results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{trial_result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")