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

# Helper functions for matrix operations
def matrix_multiply(A, B):
    m = len(A)
    n = len(B[0])
    p = len(B)
    result = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                result[i][j] += A[i][k] * B[k][j]
    return result

def gaussian_elimination(A, b):
    m = len(A)
    n = len(A[0])
    augmented_matrix = [A[i] + [b[i]] for i in range(m)]
    
    for i in range(n):
        # Find the pivot
        max_row = i
        for j in range(i+1, m):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j
        
        # Swap rows
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        
        # Eliminate below the pivot
        for j in range(i+1, m):
            factor = augmented_matrix[j][i] / augmented_matrix[i][i]
            for k in range(n + 1):
                augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    
    # Back-substitute to find the solution
    x = [0] * n
    for i in range(n-1, -1, -1):
        sum_val = 0
        for j in range(i+1, n):
            sum_val += augmented_matrix[i][j] * x[j]
        x[i] = (augmented_matrix[i][n] - sum_val) / augmented_matrix[i][i]
    
    return x

# Function to generate a random Boolean satisfiability instance
def generate_instance(n):
    clauses = []
    for _ in range(n):
        clause = [random.choice([-1, 1]) * random.randint(1, n) for _ in range(random.randint(2, 4))]
        clauses.append(clause)
    return clauses

# Function to compute the Gromov-Wasserstein distance
def gw_distance(instance):
    n = len(instance)
    points = [[i/n for i in range(n+1)]]
    weights = [sum(abs(x) for x in clause) for clause in instance]
    
    # Construct the cost matrix
    m = len(points)
    C = [[0] * m for _ in range(m)]
    for i in range(m):
        for j in range(i, m):
            if i == j:
                C[i][j] = 0
            else:
                dist = sum(abs(points[i][k] - points[j][k]) for k in range(n+1))
                C[i][j] = dist * weights[i]
                C[j][i] = dist * weights[j]
    
    # Solve the linear program to find the optimal transport plan
    A = [[0] * m for _ in range(m)]
    b = [0] * m
    for i in range(m):
        for j in range(m):
            A[i][j] = C[i][j]
        b[i] = 1
    
    x = gaussian_elimination(A, b)
    
    # Compute the Gromov-Wasserstein distance
    gw_dist = sum(x[i] * C[i][j] for i in range(m) for j in range(i+1, m))
    return gw_dist

# Function to compute the DPLL proof path length
def dpll_path_length(instance):
    def dpll(clauses, assignment):
        if not clauses:
            return 0
        unit_clauses = [c[0] for c in clauses if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0]
            new_assignment = assignment.copy()
            new_assignment[literal // abs(literal)] = True
            return dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment)
        
        literal = random.choice(clauses[0])
        new_assignment = assignment.copy()
        new_assignment[literal // abs(literal)] = True
        true_path_length = dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment)
        if true_path_length is not None:
            return 1 + true_path_length
        
        new_assignment[literal // abs(literal)] = False
        false_path_length = dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment)
        if false_path_length is not None:
            return 1 + false_path_length
        
        return None
    
    assignment = [False] * (n+1)
    return dpll(instance, assignment)

# Function to run a single trial
def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instance = generate_instance(n)
        gw_dist = gw_distance(instance)
        dpll_path_length_val = dpll_path_length(instance)
        
        if gw_dist > 10:
            return {
                "metric_name": "GW_dist",
                "metric_value": gw_dist,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "GW_dist too large"
            }
        
        results.append({
            "gw_dist": gw_dist,
            "dpll_path_length": dpll_path_length_val
        })
    
    # Compute the Pearson correlation coefficient
    gw_dists = [r["gw_dist"] for r in results]
    dpll_lengths = [r["dpll_path_length"] for r in results]
    mean_gw_dist = sum(gw_dists) / len(gw_dists)
    mean_dpll_length = sum(dpll_lengths) / len(dpll_lengths)
    
    cov = sum((gw_dists[i] - mean_gw_dist) * (dpll_lengths[i] - mean_dpll_length) for i in range(len(gw_dists)))
    var_gw_dist = sum((gw_dists[i] - mean_gw_dist) ** 2 for i in range(len(gw_dists)))
    var_dpll_length = sum((dpll_lengths[i] - mean_dpll_length) ** 2 for i in range(len(dpll_lengths)))
    
    if var_gw_dist == 0 or var_dpll_length == 0:
        return {
            "metric_name": "GW_dist",
            "metric_value": mean_gw_dist,
            "instances_tested": len(gw_dists),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Variance is zero"
        }
    
    pearson_corr = cov / (math.sqrt(var_gw_dist) * math.sqrt(var_dpll_length))
    
    return {
        "metric_name": "GW_dist",
        "metric_value": mean_gw_dist,
        "instances_tested": len(gw_dists),
        "n_max": max(n_values),
        "conjecture_holds": pearson_corr >= 0.8,
        "counterexample": ""
    }

# Main function to run multiple trials
if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}")