# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def generate_random_formula(n):
    variables = [f'x{i}' for i in range(n)]
    clauses = []
    for _ in range(n):
        clause = random.sample(variables, random.randint(1, n))
        clauses.append(' OR '.join(clause))
    return ' AND '.join(clauses)

def evaluate_formula(formula, assignment):
    stack = []
    tokens = formula.split()
    for token in tokens:
        if token == 'AND':
            b = stack.pop()
            a = stack.pop()
            stack.append(a and b)
        elif token == 'OR':
            b = stack.pop()
            a = stack.pop()
            stack.append(a or b)
        else:
            stack.append(assignment[token[1:]] if token.startswith('x') else not assignment[token[1:]])
    return stack[0]

def satisfiability_degree(formula):
    n = len(formula.split())
    variables = [f'x{i}' for i in range(n)]
    max_satisfying_assignments = 0
    for _ in range(2**n):
        assignment = {var: bool(random.randint(0, 1)) for var in variables}
        if evaluate_formula(formula, assignment):
            max_satisfying_assignments += 1
    return max_satisfying_assignments

def tropicalization_order(graph):
    n = len(graph)
    adj_matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if graph[i][j]:
                adj_matrix[i][j] = 1
                adj_matrix[j][i] = 1
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for i in range(rows):
            max_row = i
            for j in range(i+1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            if matrix[i][i] == 0:
                continue
            rank += 1
            for j in range(i+1, cols):
                matrix[i][j] /= matrix[i][i]
            for k in range(rows):
                if k != i and matrix[k][i] != 0:
                    factor = -matrix[k][i]
                    for j in range(i, cols):
                        matrix[k][j] += factor * matrix[i][j]
        return rank
    
    return gaussian_elimination(adj_matrix)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):
            formula = generate_random_formula(n)
            order = tropicalization_order(formula)
            degree = satisfiability_degree(formula)
            if order is not None and degree is not None:
                metric_values.append((order, degree))
                instances_tested += 1
                n_max = max(n_max, n)
    
    if len(metric_values) < 30:
        return {
            "metric_name": "Tropicalization Order vs Satisfiability Degree",
            "metric_value": None,
            "instances_tested": len(metric_values),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Not enough instances tested"
        }
    
    tau = [x[0] for x in metric_values]
    D = [x[1] for x in metric_values]
    mean_tau = sum(tau) / len(tau)
    mean_D = sum(D) / len(D)
    std_tau = (sum((x - mean_tau)**2 for x in tau) / len(tau))**0.5
    std_D = (sum((x - mean_D)**2 for x in D) / len(D))**0.5
    
    correlation_coefficient = sum((tau[i] - mean_tau) * (D[i] - mean_D) for i in range(len(tau))) / (len(tau) * std_tau * std_D)
    
    return {
        "metric_name": "Tropicalization Order vs Satisfiability Degree",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and max(abs(tau[i] - D[i]) for i in range(len(tau))) <= 1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(x["metric_value"] for x in results if x["metric_value"] is not None) / len(results)
    std_metric_value = (sum((x["metric_value"] - mean_metric_value)**2 for x in results if x["metric_value"] is not None) / len(results))**0.5
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    if all(x["conjecture_holds"] for x in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for x in results if not x["conjecture_holds"]) >= 8:
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={seeds[next(i for i, x in enumerate(results) if not x['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")