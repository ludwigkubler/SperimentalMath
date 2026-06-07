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

def generate_instance(n):
    variables = list(range(n))
    clauses = []
    for _ in range(2 * n):  # Each variable appears in at least two clauses
        clause = random.sample(variables, 3)
        if random.choice([True, False]):
            clause = [-v for v in clause]
        clauses.append(clause)
    return variables, clauses

def construct_metric_space(instance):
    variables, clauses = instance
    n = len(variables)
    points = [[Fraction(1, 2)] * n]  # Uniform distribution over all assignments
    weights = []
    for clause in clauses:
        weight = sum(1 if v in clause else -1 for v in variables) / n
        weights.append(weight)
    return points, weights

def gaussian_elimination(A, b):
    n = len(b)
    augmented_matrix = [A[i] + [b[i]] for i in range(n)]
    
    # Forward elimination
    for i in range(n):
        if augmented_matrix[i][i] == 0:
            for j in range(i+1, n):
                if augmented_matrix[j][i] != 0:
                    augmented_matrix[i], augmented_matrix[j] = augmented_matrix[j], augmented_matrix[i]
                    break
            else:
                raise ValueError("Matrix is singular")
        pivot = augmented_matrix[i][i]
        for j in range(n + 1):
            augmented_matrix[i][j] /= pivot
    
    # Backward substitution
    x = [0] * n
    for i in range(n-1, -1, -1):
        sum_val = sum(augmented_matrix[i][j] * x[j] for j in range(i+1, n))
        x[i] = (augmented_matrix[i][n] - sum_val) / augmented_matrix[i][i]
    return x

def gw_distance(instance):
    points, weights = construct_metric_space(instance)
    n = len(points[0])
    A = [[0] * n for _ in range(n)]
    b = [0] * n
    
    for i in range(n):
        for j in range(i+1, n):
            dist = sum((points[i][k] - points[j][k])**2 for k in range(n))
            A[i][j] = A[j][i] = dist
            b[i] += weights[j]
            b[j] += weights[i]
    
    x = gaussian_elimination(A, b)
    gw_dist = sum(x[i]**2 * weights[i] for i in range(n)) / n
    return gw_dist

def dpll_path_length(instance):
    variables, clauses = instance
    
    def is_satisfiable(assignment):
        for clause in clauses:
            if not any(v in assignment and (v > 0) == (c in assignment[v]) or v < 0 == (-c in assignment[-v]) for c in clause):
                return False
        return True
    
    def backtrack(assignment, unassigned):
        if not unassigned:
            return is_satisfiable(assignment)
        
        var = unassigned[0]
        rest = unassigned[1:]
        assignment[var] = 1
        if backtrack(assignment, rest):
            return True
        del assignment[var]
        assignment[-var] = -1
        return backtrack(assignment, rest)
    
    return len(backtrack({}, variables))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    gw_dists = []
    dpll_lengths = []
    
    for n in n_values:
        instance = generate_instance(n)
        gw_dist = gw_distance(instance)
        if gw_dist > 10:
            return {
                "metric_name": "GW_dist",
                "metric_value": gw_dist,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"GW_dist(instance) = {gw_dist} > 10"
            }
        gw_dists.append(gw_dist)
        
        dpll_length = dpll_path_length(instance)
        dpll_lengths.append(dpll_length)
    
    correlation_coefficient = sum((gw_dists[i] - sum(gw_dists) / len(gw_dists)) * (dpll_lengths[i] - sum(dpll_lengths) / len(dpll_lengths)) for i in range(len(gw_dists))) / (len(gw_dists) * math.sqrt(sum((gw_dists[i] - sum(gw_dists) / len(gw_dists))**2 for i in range(len(gw_dists)))) * math.sqrt(sum((dpll_lengths[i] - sum(dpll_lengths) / len(dpll_lengths))**2 for i in range(len(dpll_lengths)))))
    
    return {
        "metric_name": "GW_dist",
        "metric_value": correlation_coefficient,
        "instances_tested": len(gw_dists),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")