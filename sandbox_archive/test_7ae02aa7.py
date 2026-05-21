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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            for j in range(cols):
                if j != i:
                    factor = matrix[j][i] / matrix[i][i]
                    for k in range(rows):
                        matrix[j][k] -= factor * matrix[i][k]
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    def compute_beta_1(vertices, edges, triangles):
        V, E, F = len(vertices), len(edges), len(triangles)
        beta_0 = 1
        boundary_matrix = [[0] * (E + F) for _ in range(E)]
        for i, (C, D) in enumerate(edges):
            boundary_matrix[i][i] = -1
            boundary_matrix[i][i + E] = 1
        for j, (A, B) in enumerate(triangles):
            boundary_matrix[j + E][j] = -1
            boundary_matrix[j + E][j + F] = 1
        rank_boundary = gaussian_elimination(boundary_matrix)
        return (E - V + beta_0) - rank_boundary
    
    def dpll(clauses, assignment):
        if not clauses:
            return True
        clause = next(c for c in clauses if any(var in c for var in assignment))
        pos_var = next(var for var in clause if var not in assignment)
        neg_var = -pos_var
        
        # Try assigning the positive literal
        new_assignment = assignment.copy()
        new_assignment[pos_var] = True
        if dpll([c for c in clauses if not (set(c) & {pos_var, neg_var})], new_assignment):
            return True
        
        # Try assigning the negative literal
        new_assignment[neg_var] = True
        if dpll([c for c in clauses if not (set(c) & {neg_var, pos_var})], new_assignment):
            return True
        
        return False
    
    def parse_php(n):
        clauses = []
        for i in range(1, n + 2):
            clause = [i]
            for j in range(i + 1, n + 2):
                clause.append(-j)
            clauses.append(clause)
        return clauses
    
    n_values = [3, 4, 5]
    results = []
    
    for n in n_values:
        clauses = parse_php(n)
        instances_tested = 0
        beta_1_sum = 0
        
        for _ in range(30):
            variable_ordering = random.sample(range(1, n + 2), n)
            assignment = {var: False for var in variable_ordering}
            
            if dpll(clauses, assignment):
                instances_tested += 1
                beta_1 = compute_beta_1(variable_ordering, [], [])
                beta_1_sum += beta_1
            
            if beta_1 < n * math.log2(n + 1):
                return {
                    "metric_name": "beta_1",
                    "metric_value": beta_1,
                    "instances_tested": instances_tested,
                    "conjecture_holds": False,
                    "counterexample": f"n={n}, beta_1={beta_1} < {n * math.log2(n + 1)}"
                }
        
        if instances_tested == 0:
            return {
                "metric_name": "beta_1",
                "metric_value": None,
                "instances_tested": instances_tested,
                "conjecture_holds": False,
                "counterexample": "No valid resolution found"
            }
        
        beta_1_avg = beta_1_sum / instances_tested
        results.append((n, beta_1_avg))
    
    if not all(beta_1 >= n * math.log2(n + 1) for n, beta_1 in results):
        return {
            "metric_name": "beta_1",
            "metric_value": None,
            "instances_tested": sum(1 for _, _ in results),
            "conjecture_holds": False,
            "counterexample": "Some beta_1 values are less than n * log2(n + 1)"
        }
    
    if len(results) < 3:
        return {
            "metric_name": "beta_1",
            "metric_value": None,
            "instances_tested": sum(1 for _, _ in results),
            "conjecture_holds": False,
            "counterexample": "Not enough data points"
        }
    
    beta_1_means = [beta_1 for n, beta_1 in results]
    beta_1_variances = [(beta_1 - sum(beta_1_means) / len(beta_1_means)) ** 2 for beta_1 in beta_1_means]
    
    return {
        "metric_name": "beta_1",
        "metric_value": sum(beta_1_means) / len(beta_1_means),
        "instances_tested": sum(1 for _, _ in results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 89, 3))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    beta_1_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    instances_tested = sum(r["instances_tested"] for r in results)
    conjecture_holds = all(r["conjecture_holds"] for r in results)
    support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
    
    if conjecture_holds and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(beta_1_values) / instances_tested} std={math.sqrt(sum(beta_1_variances) / len(beta_1_variances))} support_fraction={support_fraction}")
    elif not conjecture_holds:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"beta_1 < n * log2(n + 1)\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")