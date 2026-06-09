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
    
    def generate_cnf(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, random.randint(1, n))
            clauses.append(clause)
        return clauses
    
    def construct_coxeter_matrix(clauses):
        n = max(max(clause) for clause in clauses)
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in clauses:
            for i in range(len(clause)):
                for j in range(i + 1, len(clause)):
                    matrix[clause[i]][clause[j]] += 1
                    matrix[clause[j]][clause[i]] += 1
        return matrix
    
    def max_rank(matrix):
        n = len(matrix)
        augmented_matrix = [row[:] + [1] for row in matrix]
        augmented_matrix.append([0] * (n + 1) + [1])
        
        def gaussian_elimination(mat):
            rows, cols = len(mat), len(mat[0]) - 1
            for i in range(rows):
                if mat[i][i] == 0:
                    for j in range(i + 1, rows):
                        if mat[j][i] != 0:
                            mat[i], mat[j] = mat[j], mat[i]
                            break
                if mat[i][i] != 0:
                    for j in range(cols + 1):
                        mat[i][j] /= mat[i][i]
                    for j in range(rows):
                        if j == i:
                            continue
                        factor = mat[j][i]
                        for k in range(cols + 1):
                            mat[j][k] -= factor * mat[i][k]
            return mat
        
        gaussian_elimination(augmented_matrix)
        
        rank = 0
        for row in augmented_matrix:
            if any(row[i] != 0 for i in range(n)):
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = random.randint(1, n * (n - 1) // 2)
        cnf = generate_cnf(n, m)
        matrix = construct_coxeter_matrix(cnf)
        rank = max_rank(matrix)
        
        if rank > 2 * m:
            return {
                "metric_name": "max_rank",
                "metric_value": rank,
                "instances_tested": len(n_values),
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "rank > 2 * clause_complexity"
            }
        
        results.append({
            "n": n,
            "m": m,
            "rank": rank
        })
    
    correlation = calculate_correlation([r["rank"] for r in results], [r["m"] for r in results])
    
    return {
        "metric_name": "max_rank",
        "metric_value": correlation,
        "instances_tested": len(n_values),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": correlation >= 0.8 and all(r["rank"] <= 2 * r["m"] for r in results),
        "counterexample": ""
    }

def calculate_correlation(x, y):
    n = len(x)
    if n < 2:
        return 0
    
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    
    cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
    var_x = sum((x[i] - mean_x) ** 2 for i in range(n)) / n
    var_y = sum((y[i] - mean_y) ** 2 for i in range(n)) / n
    
    if var_x == 0 or var_y == 0:
        return 0
    
    return cov_xy / (math.sqrt(var_x) * math.sqrt(var_y))

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank > 2 * clause_complexity\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")