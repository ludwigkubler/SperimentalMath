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
        factor = Fraction(matrix[i][i])
        for j in range(i, n + 1):
            matrix[i][j] /= factor
        for j in range(n):
            if i != j:
                factor = Fraction(matrix[j][i])
                for k in range(i, n + 1):
                    matrix[j][k] -= factor * matrix[i][k]
    return matrix

def determinant(matrix):
    n = len(matrix)
    det = Fraction(1)
    for i in range(n):
        det *= matrix[i][i]
    return det

def tseitin_formula(n):
    variables = [f'x{i+1}' for i in range(n)]
    clauses = []
    for i in range(n):
        y = f'y{i+1}'
        clauses.append([variables[i], -y])
        clauses.append([-variables[i], y])
        for j in range(i+1, n):
            z = f'z{(i+1)*(n-i)//2+j-i-1}'
            clauses.append([y, z])
            clauses.append([-y, -z])
            clauses.append([z, variables[j]])
            clauses.append([-z, -variables[j]])
    return variables, clauses

def resolution_width(clauses):
    n = len(clauses)
    max_clauses = 0
    for i in range(n):
        for j in range(i+1, n):
            new_clauses = []
            for clause_i in clauses[i]:
                if -clause_i in clauses[j]:
                    continue
                for clause_j in clauses[j]:
                    if -clause_j in clauses[i]:
                        continue
                    new_clause = list(set(clause_i + clause_j))
                    if len(new_clause) == 1:
                        return 1
                    new_clauses.append(new_clause)
            max_clauses = max(max_clauses, len(new_clauses))
    return max_clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        variables, clauses = tseitin_formula(n)
        i_phi = len(clauses)  # Simplified local indeterminacy measure
        w_phi = resolution_width(clauses)
        
        if i_phi == 0 or w_phi == 0:
            continue
        
        results.append({
            "n": n,
            "i_phi": i_phi,
            "w_phi": w_phi
        })
    
    if not results:
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    instances_tested = len(results)
    n_max = max(result["n"] for result in results)
    i_phi_values = [result["i_phi"] for result in results]
    w_phi_values = [result["w_phi"] for result in results]
    
    mean_i_phi = sum(i_phi_values) / instances_tested
    mean_w_phi = sum(w_phi_values) / instances_tested
    
    correlation_coefficient = 0
    if len(results) > 1:
        numerator = sum((i_phi - mean_i_phi) * (w_phi - mean_w_phi) for i_phi, w_phi in zip(i_phi_values, w_phi_values))
        denominator = math.sqrt(sum((i_phi - mean_i_phi)**2 for i_phi in i_phi_values)) * math.sqrt(sum((w_phi - mean_w_phi)**2 for w_phi in w_phi_values))
        correlation_coefficient = numerator / denominator
    
    conjecture_holds = correlation_coefficient >= 0.8
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.8"
    
    return {
        "metric_name": "resolution_width",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        mean_value = None
        std_dev = None
        support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        counterexample = next(r["counterexample"] for r in results if "counterexample" in r)
        first_failing_seed = seeds[next(i for i, r in enumerate(results) if "counterexample" in r)]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")