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
    
    def generate_graph(n):
        return [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, n):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def rank(A):
        A = gaussian_elimination(A)
        rank = 0
        for row in A:
            if any(row):
                rank += 1
        return rank
    
    def dpll(graph, assignment, clause_set, clause_index):
        n = len(graph)
        if clause_index == len(clause_set):
            return True
        clause = clause_set[clause_index]
        for i in range(n):
            if graph[i][i] == 1 and i not in assignment:
                new_assignment = assignment + [i]
                if dpll(graph, new_assignment, clause_set, clause_index + 1):
                    return True
        return False
    
    def height_dpll(graph):
        n = len(graph)
        assignment = []
        clause_set = [[i for i in range(n) if graph[i][i] == 1]]
        return dpll(graph, assignment, clause_set, 0)
    
    def min_categorical_dimension(graph):
        n = len(graph)
        A = [[0] * (n + 2) for _ in range(n + 2)]
        for i in range(n):
            for j in range(n):
                if graph[i][j]:
                    A[i][j+1] = 1
                    A[j+1][i] = 1
        A[n][n+1] = 1
        A[n+1][n] = 1
        return rank(A)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        graph = generate_graph(n)
        min_dim = min_categorical_dimension(graph)
        height = height_dpll(graph)
        results.append((min_dim, height))
    
    if len(results) < 30:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x)**2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y)**2 for i in range(n)) / n)
        return cov_xy / (std_x * std_y) if std_x * std_y != 0 else None
    
    x, y = zip(*results)
    corr_coeff = pearson_correlation(x, y)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": corr_coeff,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": corr_coeff is not None and abs(corr_coeff) >= 0.8,
        "counterexample": "" if corr_coeff is not None else "no_correlation"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_corr_coeff = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='no_correlation' first_failing_seed={first_failing_seed}")