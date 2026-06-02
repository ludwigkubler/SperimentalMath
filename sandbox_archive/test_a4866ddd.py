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
        # Find pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate non-pivot elements
        pivot = matrix[i][i]
        for j in range(i, n):
            matrix[i][j] /= pivot
        for k in range(n):
            if k != i:
                factor = matrix[k][i]
                for j in range(i, n):
                    matrix[k][j] -= factor * matrix[i][j]

def matrix_multiplication(A, B):
    m = len(A)
    n = len(B[0])
    p = len(B)
    result = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                result[i][j] += A[i][k] * B[k][j]
    return result

def determinant(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    det = 0
    for j in range(n):
        minor = [row[:j] + row[j+1:] for row in matrix[1:]]
        det += (-1) ** j * matrix[0][j] * determinant(minor)
    return det

def minimal_order(clauses):
    n = len(clauses)
    m = 2 * n
    A = [[0 for _ in range(m)] for _ in range(m)]
    b = [0 for _ in range(m)]
    
    tseitin_vars = {}
    var_count = 1
    
    def add_clause(var1, var2):
        nonlocal var_count
        if var1 not in tseitin_vars:
            tseitin_vars[var1] = var_count
            var_count += 1
        if var2 not in tseitin_vars:
            tseitin_vars[var2] = var_count
            var_count += 1
        
        A[tseitin_vars[var1]-n][tseitin_vars[var2]-n] = -1
        A[tseitin_vars[var2]-n][tseitin_vars[var1]-n] = 1
        b[tseitin_vars[var1]-n] -= 1
        b[tseitin_vars[var2]-n] += 1
    
    for clause in clauses:
        if len(clause) == 1:
            add_clause(clause[0], -clause[0])
        else:
            var1 = clause[0]
            for i in range(1, len(clause)):
                var2 = clause[i]
                add_clause(var1, -var2)
    
    A = matrix_multiplication(A, A)
    gaussian_elimination(A)
    
    rank = sum(1 for row in A if any(x != 0 for x in row))
    return m - rank

def tseitin_formula(clauses):
    n = len(clauses)
    m = 2 * n
    formula = []
    
    tseitin_vars = {}
    var_count = 1
    
    def add_clause(var1, var2):
        nonlocal var_count
        if var1 not in tseitin_vars:
            tseitin_vars[var1] = var_count
            var_count += 1
        if var2 not in tseitin_vars:
            tseitin_vars[var2] = var_count
            var_count += 1
        
        formula.append([tseitin_vars[var1], -var2])
        formula.append([-tseitin_vars[var1], var2])
    
    for clause in clauses:
        if len(clause) == 1:
            formula.append([clause[0]])
        else:
            var1 = clause[0]
            for i in range(1, len(clause)):
                var2 = clause[i]
                add_clause(var1, -var2)
    
    return formula

def circuit_monotone_width(circuit):
    n = len(circuit)
    width = 0
    stack = []
    
    for gate in circuit:
        if gate[0] == 'AND':
            stack.append(gate[1:])
        elif gate[0] == 'OR':
            while len(stack[-1]) > 1:
                stack.pop()
            stack.append(gate[1:])
        else:
            stack.pop()
    
    return max(len(x) for x in stack)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 0
    metric_value = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            clauses = []
            for _ in range(n):
                clause = random.sample([-i-1 for i in range(n)], random.randint(1, n))
                clauses.append(clause)
            
            formula = tseitin_formula(clauses)
            m_Cphi = minimal_order(formula)
            w_Cphi = circuit_monotone_width(circuit)
            
            if m_Cphi > 10:
                return {
                    "metric_name": "minimal_order",
                    "metric_value": m_Cphi,
                    "instances_tested": instances_tested,
                    "n_max": n_max,
                    "conjecture_holds": False,
                    "counterexample": f"m(Cφ) > 10 for n={n}, m(Cφ)={m_Cphi}"
                }
            
            if w_Cphi == 0:
                continue
            
            instances_tested += 1
            metric_value += m_Cphi / w_Cphi
    
    mean_metric = metric_value / instances_tested
    support_fraction = instances_tested / (n_max * len([5, 10, 15, 20, 30, 40]))
    
    if support_fraction >= 0.8:
        return {
            "metric_name": "minimal_order",
            "metric_value": mean_metric,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "minimal_order",
            "metric_value": mean_metric,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": f"support_fraction={support_fraction}"
        }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric = sum(x["metric_value"] for x in results) / len(results)
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std=0 support_fraction={support_fraction}")
    elif any(x["counterexample"] != "" for x in results):
        counterexamples = [x["counterexample"] for x in results if x["counterexample"] != ""]
        first_failing_seed = next(x["seed"] for x in results if x["conjecture_holds"] is False)
        print(f"RESULT: FALSIFIED counterexample=\"{' '.join(counterexamples)}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")