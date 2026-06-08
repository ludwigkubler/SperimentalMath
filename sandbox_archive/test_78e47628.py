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

def generate_boolean_circuit(depth):
    if depth == 1:
        return ['0', '1']
    left = generate_boolean_circuit(depth - 1)
    right = generate_boolean_circuit(depth - 1)
    return [f'({l} AND {r})' for l in left] + [f'({l} OR {r})' for l in left]

def evaluate_circuit(circuit, assignment):
    if isinstance(circuit, str):
        if circuit == '0':
            return False
        elif circuit == '1':
            return True
        else:
            var = circuit[1:-2]
            op = circuit[2:-2]
            left = evaluate_circuit(circuit[3:-4], assignment)
            right = evaluate_circuit(circuit[-3:], assignment)
            if op == 'AND':
                return left and right
            elif op == 'OR':
                return left or right
    else:
        return all(evaluate_circuit(subcircuit, assignment) for subcircuit in circuit)

def tseitin_formula(circuit):
    variables = set()
    clauses = []
    
    def tseitin_helper(expr, var_id):
        nonlocal variables, clauses
        if expr == '0':
            return 0
        elif expr == '1':
            return 1
        else:
            var = expr[1:-2]
            op = expr[2:-2]
            left = tseitin_helper(expr[3:-4], var_id)
            right = tseitin_helper(expr[-3:], var_id + 1)
            if op == 'AND':
                new_var = f'v{var_id}'
                clauses.append([new_var, -left])
                clauses.append([new_var, -right])
                clauses.append([-new_var, left, right])
                variables.add(new_var)
                return new_var
            elif op == 'OR':
                new_var = f'v{var_id}'
                clauses.append([new_var, -left])
                clauses.append([new_var, -right])
                clauses.append([-new_var, left])
                clauses.append([-new_var, right])
                variables.add(new_var)
                return new_var
    
    tseitin_helper(circuit, 0)
    return variables, clauses

def gaussian_elimination(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    
    for i in range(rows):
        # Find the pivot row
        max_row = i
        for j in range(i + 1, rows):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        
        # Swap rows
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below the pivot
        for j in range(i + 1, rows):
            factor = matrix[j][i] / matrix[i][i]
            for k in range(cols):
                matrix[j][k] -= factor * matrix[i][k]
    
    # Back-substitute to find the solution
    solution = [0] * cols
    for i in range(rows - 1, -1, -1):
        solution[i] = matrix[i][-1]
        for j in range(i + 1, cols):
            solution[i] -= matrix[i][j] * solution[j]
        solution[i] /= matrix[i][i]
    
    return solution

def minimal_local_index(clauses):
    n = len(clauses)
    m = len(clauses[0])
    matrix = [[0] * (m + 1) for _ in range(n)]
    
    for i, clause in enumerate(clauses):
        for j in clause:
            if j > 0:
                matrix[i][j - 1] += 1
            else:
                matrix[i][-1] -= 1
    
    solution = gaussian_elimination(matrix)
    return sum(abs(x) for x in solution)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    depths = [5, 10, 15, 20, 30, 40]
    metric_values = []
    instances_tested = 0
    n_max = 0
    
    for depth in depths:
        circuit = generate_boolean_circuit(depth)
        variables, clauses = tseitin_formula(circuit)
        msl = minimal_local_index(clauses)
        
        if msl > 4 * depth * math.log(len(variables)):
            return {
                "metric_name": "Minimal Local Index",
                "metric_value": msl,
                "instances_tested": instances_tested,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": f"Vertex's local index exceeds 4d log n for depth {depth}"
            }
        
        metric_values.append(msl)
        instances_tested += len(clauses)
        n_max = max(n_max, depth)
    
    correlation_coefficient = sum((x - mean) * (y - mean) for x, y in zip(metric_values, depths)) / \
                              math.sqrt(sum((x - mean) ** 2 for x in metric_values) * sum((y - mean) ** 2 for y in depths))
    mean = sum(metric_values) / len(metric_values)
    
    return {
        "metric_name": "Minimal Local Index",
        "metric_value": mean,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, {trial_result}}}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and any(result["metric_value"] < 0.5 for result in results):
        print("RESULT: FALSIFIED counterexample=\"Pearson correlation coefficient < 0.5\" first_failing_seed=<s>")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")