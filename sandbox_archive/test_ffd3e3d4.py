# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations

def generate_cnf(n, m):
    clauses = []
    for _ in range(m):
        clause = [random.randint(1, n) * (2 * random.choice([1, -1]) - 1) for _ in range(random.randint(1, n))]
        clauses.append(clause)
    return clauses

def incidence_algebra(cnf):
    n = max(abs(lit) for lit in cnf[0])
    algebra = [[0] * (n + 1) for _ in range(n + 1)]
    for clause in cnf:
        for i in clause:
            for j in clause:
                if i != j:
                    algebra[abs(i)][abs(j)] += 1
    return algebra

def deligne_lusztig_tree_depth(algebra):
    n = len(algebra) - 1
    visited = [False] * (n + 1)
    
    def dfs(node, depth=0):
        if visited[node]:
            return depth
        visited[node] = True
        max_child_depth = 0
        for i in range(1, n + 1):
            if algebra[node][i] > 0:
                child_depth = dfs(i, depth + 1)
                if child_depth > max_child_depth:
                    max_child_depth = child_depth
        return max_child_depth
    
    max_depth = 0
    for i in range(1, n + 1):
        node_depth = dfs(i)
        if node_depth > max_depth:
            max_depth = node_depth
    return max_depth

def communication_complexity_rank_variance(cnf):
    n = len(cnf[0])
    rank_matrix = [[0] * (n + 1) for _ in range(n + 1)]
    for clause in cnf:
        for i in clause:
            for j in clause:
                if i != j:
                    rank_matrix[abs(i)][abs(j)] += 1
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for k in range(i + 1, n):
                if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                    max_row = k
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            for j in range(i + 1, n):
                factor = Fraction(matrix[j][i], matrix[i][i])
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
        
        rank = 0
        for i in range(n):
            if all(x == 0 for x in matrix[i]):
                continue
            rank += 1
        return rank
    
    row_rank = gaussian_elimination(rank_matrix)
    col_rank = gaussian_elimination([list(row) for row in zip(*rank_matrix)])
    return (row_rank - col_rank) ** 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_max = 40
    instances_tested = 30
    depths = []
    variances = []
    
    for _ in range(instances_tested):
        m = random.randint(1, n_max * 2)
        cnf = generate_cnf(n_max, m)
        
        algebra = incidence_algebra(cnf)
        depth = deligne_lusztig_tree_depth(algebra)
        variance = communication_complexity_rank_variance(cnf)
        
        depths.append(depth)
        variances.append(variance)
    
    correlation_coefficient = sum((depths[i] - mean_depth) * (variances[i] - mean_variance) for i in range(instances_tested)) / instances_tested
    mean_depth = sum(depths) / instances_tested
    mean_variance = sum(variances) / instances_tested
    
    conjecture_holds = correlation_coefficient > 0.95
    counterexample = "" if conjecture_holds else f"Correlation coefficient {correlation_coefficient:.4f} < 0.95"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
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
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient below 0.95\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")