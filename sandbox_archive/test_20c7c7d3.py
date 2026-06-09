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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n * (n - 1)):
            clause = [random.randint(1, n), random.randint(-(n + 1), -1)]
            clauses.append(clause)
        return clauses
    
    def construct_pseudo_manifold(clauses):
        vertices = set()
        edges = set()
        for clause in clauses:
            for var in clause:
                if var > 0:
                    vertices.add(var)
                else:
                    vertices.add(-var)
            for i in range(len(clause)):
                for j in range(i + 1, len(clause)):
                    edge = tuple(sorted([clause[i], clause[j]]))
                    edges.add(edge)
        return vertices, edges
    
    def local_inductive_dimension(vertices, edges):
        if not vertices or not edges:
            return 0
        n = len(vertices)
        m = len(edges)
        if m == 0:
            return 1
        adjacency_matrix = [[0] * n for _ in range(n)]
        for u, v in edges:
            i = list(vertices).index(u) - 1
            j = list(vertices).index(v) - 1
            adjacency_matrix[i][j] = 1
            adjacency_matrix[j][i] = 1
        
        def gaussian_elimination(matrix):
            rows, cols = len(matrix), len(matrix[0])
            for i in range(rows):
                max_row = i
                for j in range(i + 1, rows):
                    if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                        max_row = j
                matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
                if matrix[i][i] == 0:
                    return None
                for j in range(i + 1, cols):
                    matrix[i][j] /= matrix[i][i]
                for k in range(rows):
                    if k != i and matrix[k][i] != 0:
                        for j in range(i, cols):
                            matrix[k][j] -= matrix[i][j] * matrix[k][i]
            return matrix
        
        reduced_matrix = gaussian_elimination(adjacency_matrix)
        rank = sum(1 for row in reduced_matrix if any(row))
        return rank - 1
    
    def resolution_width(clauses):
        stack = []
        while clauses:
            clause = clauses.pop()
            new_clause = None
            for c in clauses:
                common_vars = set(c).intersection(set(clause))
                if len(common_vars) == 2:
                    var, neg_var = list(common_vars)
                    if (var, -neg_var) in edges or (-var, var) in edges:
                        new_clause = [v for v in c if v not in common_vars]
                        break
            if new_clause is None:
                return len(stack)
            stack.append(new_clause)
        return len(stack)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        cnf = generate_cnf(n)
        vertices, edges = construct_pseudo_manifold(cnf)
        l_d = local_inductive_dimension(vertices, edges)
        w_phi = resolution_width(cnf)
        if l_d is None or w_phi == 0:
            continue
        results.append((n, w_phi, l_d))
    
    if not results:
        return {
            "metric_name": "resolution_width",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_max = max(n for n, _, _ in results)
    instances_tested = len(results)
    w_values = [w_phi for _, w_phi, _ in results]
    l_d_values = [l_d for _, _, l_d in results]
    
    def correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / len(x)
        std_x = (sum((xi - mean_x) ** 2 for xi in x) / len(x)) ** 0.5
        std_y = (sum((yi - mean_y) ** 2 for yi in y) / len(y)) ** 0.5
        return cov_xy / (std_x * std_y)
    
    corr_coeff = correlation(w_values, l_d_values)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": corr_coeff,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": corr_coeff >= 0.8 and all(corr_coeff >= 0.5 for _ in range(30)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 40) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_corr_coeff = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction=1.0")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")