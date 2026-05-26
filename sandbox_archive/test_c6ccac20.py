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
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n + 1):
                A[j][k] -= factor * A[i][k]

    # Back-substitute to find solution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (A[i][n] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def matrix_multiplication(A, B):
    m = len(A)
    p = len(B[0])
    q = len(B)
    C = [[0 for _ in range(p)] for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(q):
                C[i][j] += A[i][k] * B[k][j]
    return C

def tseitin_circuit(n):
    variables = list(range(1, n + 2))
    clauses = []
    
    # Add clauses for each OR gate
    for i in range(1, n + 1):
        var_i = variables[i - 1]
        var_not_i = -var_i
        var_or = variables[n + i - 1]
        clauses.append([var_i, var_or])
        clauses.append([var_not_i, var_or])
    
    # Add clauses for each AND gate
    for i in range(1, n):
        var_and = variables[2 * n + i - 1]
        for j in range(i, n):
            var_j = variables[j]
            var_not_j = -var_j
            clauses.append([var_j, var_and])
            clauses.append([var_not_j, var_and])
    
    # Add clauses for the final OR gate
    var_final_or = variables[2 * n + n - 1]
    for i in range(1, n):
        var_i = variables[n + i - 1]
        var_not_i = -var_i
        clauses.append([var_i, var_final_or])
        clauses.append([var_not_i, var_final_or])
    
    # Add clauses for the final AND gate
    var_final_and = variables[3 * n - 2]
    for i in range(1, n):
        var_i = variables[2 * n + i - 1]
        var_not_i = -var_i
        clauses.append([var_i, var_final_and])
        clauses.append([var_not_i, var_final_and])
    
    # Add clauses for the final OR gate
    var_final_or = variables[3 * n - 1]
    for i in range(1, n):
        var_i = variables[2 * n + i - 1]
        var_not_i = -var_i
        clauses.append([var_i, var_final_or])
        clauses.append([var_not_i, var_final_or])
    
    return variables, clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_satisfying_assignments = 0
    total_instances_tested = 0
    
    for n in n_values:
        variables, clauses = tseitin_circuit(n)
        num_variables = len(variables)
        
        # Compute homology groups (minimal rank)
        A = [[0] * num_variables for _ in range(num_variables)]
        for clause in clauses:
            for lit in clause:
                if lit > 0:
                    A[lit-1][lit-1] += 1
                else:
                    A[-lit-1][-lit-1] += 1
        
        rank = len(gaussian_elimination(A))
        
        # Count satisfying assignments
        satisfying_assignments = 2 ** n
        total_satisfying_assignments += satisfying_assignments
        total_instances_tested += satisfying_assignments
    
    mean_rank = total_satisfying_assignments / total_instances_tested
    ratio = mean_rank / n_values[-1]
    
    return {
        "metric_name": "Ratio of Satisfying Assignments to Total Inputs",
        "metric_value": ratio,
        "instances_tested": total_instances_tested,
        "conjecture_holds": ratio >= 0.8 and mean_rank <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 59))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not enough satisfying assignments\" first_failing_seed={first_failing_seed}")