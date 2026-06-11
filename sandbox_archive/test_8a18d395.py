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
    
    def generate_formula(n, m):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, 2)
            clauses.append(clause)
        return clauses
    
    def evaluate_formula(formula, assignment):
        return all(all(assignment[var] == val for var, val in clause.items()) for clause in formula)
    
    def characteristic_polynomial(formula):
        n = len(formula[0])
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in formula:
            for i in range(n):
                if f'x{i}' not in clause:
                    matrix[i][i] += 1
                else:
                    matrix[i][i] -= 1
            matrix[n][i] = -1
        return matrix
    
    def lll_reduction(matrix):
        n, m = len(matrix), len(matrix[0])
        B = [list(row) for row in matrix]
        G = [[Fraction(0)] * m for _ in range(n)]
        U = [[Fraction(0)] * m for _ in range(m)]
        Q = [[Fraction(0)] * m for _ in range(m)]
        
        def gram_schmidt(B):
            for i in range(n):
                B[i] /= norm(B[i])
                for j in range(i + 1, n):
                    G[j][i] = dot_product(B[j], B[i]) / norm(B[i])
                    B[j] -= G[j][i] * B[i]
        
        def gram_schmidt_update(G, U, Q, i, j):
            if i == j:
                G[j][j] = norm(B[j])
                for k in range(j + 1, n):
                    G[k][j] = dot_product(B[k], B[j]) / G[j][j]
                    B[k] -= G[k][j] * B[j]
            else:
                U[i][j] = G[j][i] / G[j][j]
                for k in range(j + 1, n):
                    G[k][j] -= U[i][j] * G[k][i]
                    B[k] -= U[i][j] * B[i]
        
        def dot_product(v1, v2):
            return sum(a * b for a, b in zip(v1, v2))
        
        def norm(v):
            return math.sqrt(sum(x**2 for x in v))
        
        gram_schmidt(B)
        G[0][0] = norm(B[0])
        Q[0][0] = 1
        
        for i in range(1, n):
            for j in range(i - 1, -1, -1):
                gram_schmidt_update(G, U, Q, i, j)
            G[i][i] = norm(B[i])
        
        return B
    
    def minimal_eichler_order(matrix):
        reduced_matrix = lll_reduction(matrix)
        det = determinant(reduced_matrix)
        return abs(det) ** (1/len(matrix))
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        elif n == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        else:
            det = Fraction(0)
            for j in range(n):
                submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
                det += (-1) ** j * matrix[0][j] * determinant(submatrix)
            return det
    
    def count_satisfying_assignments(formula, n):
        assignments = [dict(zip(range(n), assignment)) for assignment in itertools.product([False, True], repeat=n)]
        return sum(1 for assignment in assignments if evaluate_formula(formula, assignment))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    total_assignments = 0
    total_eichler_orders = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            m = random.randint(1, n)
            formula = generate_formula(n, m)
            assignments = [dict(zip(range(n), assignment)) for assignment in itertools.product([False, True], repeat=n)]
            total_assignments += len(assignments)
            eichler_order = minimal_eichler_order(characteristic_polynomial(formula))
            results.append((eichler_order, len(assignments)))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    eichler_orders = [e for e, _ in results]
    assignments_counts = [a for _, a in results]
    correlation_coefficient = pearson_correlation(eichler_orders, assignments_counts)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7 and all(abs(correlation_coefficient - other) < 0.3 for other in eichler_orders),
        "counterexample": ""
    }

def pearson_correlation(x, y):
    n = len(x)
    if n != len(y):
        raise ValueError("x and y must have the same length")
    
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    
    cov_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / n
    var_x = sum((xi - mean_x)**2 for xi in x) / n
    var_y = sum((yi - mean_y)**2 for yi in y) / n
    
    return cov_xy / (math.sqrt(var_x) * math.sqrt(var_y))

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not all(result["instances_tested"] > 0 for result in results):
        print("RESULT: INCONCLUSIVE reason=not_enough_data")
    else:
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")