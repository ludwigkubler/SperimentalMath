# auto-injected by SEC sandbox
import json
import sys
import os
import time
import re
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
import itertools
import collections

# Helper functions for Gaussian elimination and matrix operations
def gaussian_elimination(A, b):
    n = len(A)
    M = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = max(range(i, n), key=lambda k: abs(M[k][i]))
        M[i], M[max_row] = M[max_row], M[i]
        factor = Fraction(M[i][i])
        for j in range(i, n + 1):
            M[i][j] /= factor
        for k in range(n):
            if k != i:
                factor = Fraction(M[k][i])
                for j in range(i, n + 1):
                    M[k][j] -= factor * M[i][j]
    return [M[i][-1] for i in range(n)]

def matrix_multiply(A, B):
    m, k, n = len(A), len(B), len(B[0])
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] += A[i][l] * B[l][j]
    return C

def matrix_inverse(A):
    n = len(A)
    I = [[Fraction(1, 1) if i == j else Fraction(0, 1) for j in range(n)] for i in range(n)]
    M = [A[i] + I[i] for i in range(n)]
    for i in range(n):
        max_row = max(range(i, n), key=lambda k: abs(M[k][i]))
        M[i], M[max_row] = M[max_row], M[i]
        factor = Fraction(M[i][i])
        for j in range(2 * n):
            M[i][j] /= factor
        for k in range(n):
            if k != i:
                factor = Fraction(M[k][i])
                for j in range(2 * n):
                    M[k][j] -= factor * M[i][j]
    return [M[i][n:] for i in range(n)]

# Function to generate a random Boolean function
def generate_boolean_function(n, m):
    return [[random.choice([0, 1]) for _ in range(m)] for _ in range(2**n)]

# Function to compute the Tseitin formula for a given Boolean function
def tseitin_formula(boolean_func, n):
    num_vars = len(boolean_func)
    tseitin_vars = list(range(num_vars + 1, num_vars + 1 + num_vars * (num_vars - 1) // 2))
    clauses = []
    
    # Add clauses for each clause in the Boolean function
    for i in range(num_vars):
        for j in range(i + 1, num_vars):
            tseitin_var = tseitin_vars[i * (num_vars - 1) // 2 + j - i - 1]
            clauses.append([tseitin_var, boolean_func[i][j], -boolean_func[j][i]])
    
    # Add clauses for each variable
    for i in range(num_vars):
        tseitin_var = tseitin_vars[i * (num_vars - 1) // 2 + num_vars - i - 1]
        clauses.append([tseitin_var, boolean_func[i][-1], -boolean_func[-1][i]])
    
    return clauses

# Function to compute the minimal diophantine exponent
def minimal_diophantine_exponent(clauses):
    n = len(clauses)
    A = [[0] * (n + 1) for _ in range(n)]
    b = [0] * n
    
    for i, clause in enumerate(clauses):
        for l in clause:
            if l > 0:
                A[i][l - 1] += 1
            else:
                A[i][-1] -= 1
    
    return max(0, len(gaussian_elimination(A, b)))

# Function to compute the communication complexity rank variance
def communication_complexity_rank_variance(clauses):
    n = len(clauses)
    num_vars = len(set(abs(l) for clause in clauses for l in clause))
    
    # Compute the incidence matrix
    M = [[0] * (num_vars + 1) for _ in range(n)]
    var_map = {}
    var_index = 0
    
    for i, clause in enumerate(clauses):
        for l in clause:
            if abs(l) not in var_map:
                var_map[abs(l)] = var_index
                var_index += 1
            M[i][var_map[abs(l)]] += 1
    
    # Compute the rank of the incidence matrix
    rank = len(gaussian_elimination(M, [0] * (num_vars + 1)))
    
    return rank

# Function to run a single trial
def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        boolean_func = generate_boolean_function(n, n)
        tseitin_clauses = tseitin_formula(boolean_func, n)
        
        diophantine_exponent = minimal_diophantine_exponent(tseitin_clauses)
        rank_variance = communication_complexity_rank_variance(tseitin_clauses)
        
        results.append({
            "n": n,
            "diophantine_exponent": diophantine_exponent,
            "rank_variance": rank_variance
        })
    
    if not results:
        return {
            "metric_name": "minimal_diophantine_exponent",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    diophantine_values = [r["diophantine_exponent"] for r in results]
    rank_variance_values = [r["rank_variance"] for r in results]
    
    mean_diophantine = sum(diophantine_values) / len(diophantine_values)
    mean_rank_variance = sum(rank_variance_values) / len(rank_variance_values)
    
    correlation_coefficient = sum((d - mean_diophantine) * (r - mean_rank_variance) for d, r in zip(diophantine_values, rank_variance_values)) / (len(results) * math.sqrt(sum((d - mean_diophantine)**2 for d in diophantine_values) * sum((r - mean_rank_variance)**2 for r in rank_variance_values)))
    
    return {
        "metric_name": "minimal_diophantine_exponent",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": correlation_coefficient > 0.5 and correlation_coefficient < 1.0,
        "counterexample": ""
    }

# Main function to run trials
if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_below_0.8\" first_failing_seed={first_failing_seed}")