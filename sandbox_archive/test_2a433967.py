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

def generate_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = [random.randint(1, n), -random.randint(1, n)]
        if random.choice([True, False]):
            clause[0] *= -1
            clause[1] *= -1
        cnf.append(clause)
    return cnf

def incidence_algebra(cnf):
    n = max(abs(x) for x in sum(cnf, []))
    algebra = [[0] * (n + 1) for _ in range(n + 1)]
    for clause in cnf:
        for i in clause:
            for j in clause:
                if i != 0 and j != 0:
                    algebra[abs(i)][abs(j)] += 1
    return algebra

def deligne_lusztig_tree_depth(algebra):
    n = len(algebra)
    depth = [0] * (n + 1)
    visited = set()
    
    def dfs(node):
        if node in visited:
            return 0
        visited.add(node)
        max_child_depth = 0
        for i in range(1, n + 1):
            if algebra[node][i] > 0:
                child_depth = dfs(i)
                if child_depth > max_child_depth:
                    max_child_depth = child_depth
        depth[node] = max_child_depth + 1
        return depth[node]
    
    for i in range(1, n + 1):
        if i not in visited:
            dfs(i)
    
    return max(depth[1:])

def communication_complexity_rank_variance(cnf):
    n = max(abs(x) for x in sum(cnf, []))
    rank_matrix = [[0] * (n + 1) for _ in range(n + 1)]
    for clause in cnf:
        for i in clause:
            for j in clause:
                if i != 0 and j != 0:
                    rank_matrix[abs(i)][abs(j)] += 1
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            pivot = matrix[i][i]
            for j in range(n):
                matrix[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = matrix[j][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        
        rank = m
        for i in range(m - 1, -1, -1):
            if all(matrix[i][j] == 0 for j in range(n)):
                rank -= 1
        
        return rank
    
    rank = gaussian_elimination(rank_matrix)
    variance = (rank * (n - rank)) / n
    return variance

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        m = random.randint(n, n * 10)
        cnf = generate_cnf(n, m)
        
        algebra = incidence_algebra(cnf)
        depth = deligne_lusztig_tree_depth(algebra)
        variance = communication_complexity_rank_variance(cnf)
        
        results.append((depth, variance))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    depths, variances = zip(*results)
    correlation_coefficient = sum((d - mean_depth) * (v - mean_variance) for d, v in results) / len(results)
    mean_depth = sum(depths) / len(depths)
    mean_variance = sum(variances) / len(variances)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": 30,
        "n_max": max(n for n, _ in results),
        "conjecture_holds": correlation_coefficient > 0.95,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        # Default list of 30 primes
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")