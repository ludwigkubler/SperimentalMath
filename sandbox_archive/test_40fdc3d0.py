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
    
    def generate_d_regular_graph(d, n):
        if d * (n - 1) % 2 != 0 or n < d + 1:
            return None
        graph = {i: [] for i in range(n)}
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if len(graph[i]) < d and len(graph[j]) < d:
                    if (i, j) not in edges and (j, i) not in edges:
                        graph[i].append(j)
                        graph[j].append(i)
                        edges.add((i, j))
        return graph
    
    def tseitin_formula(graph):
        n = len(graph)
        literals = {i: f"x{i}" for i in range(n)}
        neg_literals = {i: f"~x{i}" for i in range(n)}
        clauses = []
        for i in range(n):
            clause = [neg_literals[i]] + [literals[j] for j in graph[i]]
            clauses.append(clause)
        return literals, neg_literals, clauses
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(n):
            if rank < m:
                pivot_row = rank
                while pivot_row < m and matrix[pivot_row][i] == 0:
                    pivot_row += 1
                if pivot_row == m:
                    continue
                matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
                for j in range(n):
                    if j != i:
                        factor = matrix[j][i] / matrix[rank][i]
                        for k in range(n):
                            matrix[j][k] -= factor * matrix[rank][k]
                rank += 1
        return rank
    
    def minimal_tropical_motivic_rank(clauses):
        n = len(clauses)
        variables = set()
        for clause in clauses:
            for literal in clause:
                if literal.startswith('x'):
                    variables.add(literal)
        matrix = [[0] * (len(variables) + 1) for _ in range(n)]
        for i, clause in enumerate(clauses):
            for literal in clause:
                if literal.startswith('x'):
                    matrix[i][list(variables).index(literal)] += 1
        return gaussian_elimination(matrix)
    
    def communication_complexity_rank(graph):
        n = len(graph)
        depth = [0] * n
        visited = set()
        
        def dfs(node, parent):
            if node in visited:
                return 0
            visited.add(node)
            max_depth = 0
            for neighbor in graph[node]:
                if neighbor != parent:
                    max_depth = max(max_depth, dfs(neighbor, node))
            depth[node] = max_depth + 1
            return depth[node]
        
        dfs(0, -1)
        return max(depth)
    
    def correlation_coefficient(mtr_C_values):
        n = len(mtr_C_values)
        mtr_sum = sum(mtr_C_values)
        C_sum = sum([x**2 for x in mtr_C_values])
        mtr_mean = mtr_sum / n
        C_mean = C_sum / n
        
        numerator = sum((mtr_C_values[i] - mtr_mean) * (i**2 - C_mean) for i in range(n))
        denominator = math.sqrt(sum((mtr_C_values[i] - mtr_mean)**2 for i in range(n))) * math.sqrt(sum((i**2 - C_mean)**2 for i in range(n)))
        
        if denominator == 0:
            return None
        
        return numerator / denominator
    
    d_values = [3, 4, 5, 6, 7, 8]
    mtr_C_values = []
    
    for d in d_values:
        n = 2 * d + 1
        graph = generate_d_regular_graph(d, n)
        if graph is None:
            continue
        
        literals, neg_literals, clauses = tseitin_formula(graph)
        mtr_C = minimal_tropical_motivic_rank(clauses)
        C = communication_complexity_rank(graph)
        
        if mtr_C is not None and C is not None:
            mtr_C_values.append(mtr_C / (C ** 2))
    
    if len(mtr_C_values) == 0:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation = correlation_coefficient(mtr_C_values)
    conjecture_holds = correlation is not None and correlation <= 1.5
    counterexample = "" if conjecture_holds else f"correlation_coefficient={correlation}"
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation,
        "instances_tested": len(mtr_C_values),
        "n_max": max(d * (2 * d + 1) for d in d_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")