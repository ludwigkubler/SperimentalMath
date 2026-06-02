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
    
    def generate_d_regular_graph(n, d):
        if (d * n) % 2 != 0:
            return None
        graph = [[] for _ in range(n)]
        edges = set()
        for i in range(d * n // 2):
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            while u == v or (u, v) in edges or (v, u) in edges:
                u = random.randint(0, n - 1)
                v = random.randint(0, n - 1)
            graph[u].append(v)
            graph[v].append(u)
            edges.add((u, v))
        return graph

    def tseitin_formula(graph):
        clauses = []
        literals = {}
        literal_count = 0
        for i in range(len(graph)):
            literals[i] = f'x{i}'
            literals[-i-1] = f'~x{i}'
        
        for i, neighbors in enumerate(graph):
            clause = [literals[i+1]]
            for neighbor in neighbors:
                clause.append(literals[neighbor+1])
                clause.append(literals[-neighbor-1])
            clauses.append(clause)
        
        for i in range(len(graph)):
            for j in range(i + 1, len(graph)):
                for k in range(j + 1, len(graph)):
                    clause = [literals[i+1], literals[j+1], literals[k+1]]
                    clause.append(literals[-i-1])
                    clause.append(literals[-j-1])
                    clause.append(literals[-k-1])
                    clauses.append(clause)
        
        return clauses

    def hodge_dimension(graph):
        n = len(graph)
        adjacency_matrix = [[0] * n for _ in range(n)]
        for i, neighbors in enumerate(graph):
            for neighbor in neighbors:
                adjacency_matrix[i][neighbor] = 1
                adjacency_matrix[neighbor][i] = 1
        
        def gaussian_elimination(matrix):
            m, n = len(matrix), len(matrix[0])
            rank = 0
            pivot_col = 0
            for i in range(m):
                if pivot_col >= n:
                    break
                max_row = i
                for j in range(i + 1, m):
                    if abs(matrix[j][pivot_col]) > abs(matrix[max_row][pivot_col]):
                        max_row = j
                matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
                if matrix[i][pivot_col] == 0:
                    pivot_col += 1
                    continue
                for j in range(i + 1, m):
                    factor = matrix[j][pivot_col] / matrix[i][pivot_col]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
                rank += 1
                pivot_col += 1
            return rank
        
        return n - gaussian_elimination(adjacency_matrix)

    def entropy(clauses):
        total_clauses = len(clauses)
        clause_counts = {}
        for clause in clauses:
            clause_str = tuple(sorted(clause))
            if clause_str in clause_counts:
                clause_counts[clause_str] += 1
            else:
                clause_counts[clause_str] = 1
        
        entropy_value = 0.0
        for count in clause_counts.values():
            probability = count / total_clauses
            entropy_value -= probability * math.log2(probability)
        
        return entropy_value

    n_values = [10, 20, 30, 40]
    results = []
    for n in n_values:
        graph = generate_d_regular_graph(n, 3)
        if graph is None:
            continue
        clauses = tseitin_formula(graph)
        hd = hodge_dimension(graph)
        H = entropy(clauses)
        results.append({"n": n, "hd": hd, "H": H})
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_max = max(result["n"] for result in results)
    correlation_coefficient = sum((result["hd"] - mean_hd) * (result["H"] - mean_H) for result in results) / len(results)
    mean_hd = sum(result["hd"] for result in results) / len(results)
    mean_H = sum(result["H"] for result in results) / len(results)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": 0.5 <= abs(correlation_coefficient) <= 1.0,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_outside_range\" first_failing_seed={first_failing_seed}")