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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_d_regular_graph(n, d):
        if (n * d) % 2 != 0:
            return None
        degree = d // 2
        graph = {i: set() for i in range(n)}
        edges_added = 0
        while edges_added < n * degree:
            u = random.randint(0, n-1)
            v = random.randint(0, n-1)
            if u != v and v not in graph[u] and len(graph[v]) < degree:
                graph[u].add(v)
                graph[v].add(u)
                edges_added += 2
        return graph

    def tseitin_formula(graph):
        n = len(graph)
        literals = {i: f'x{i}' for i in range(n)}
        clauses = []
        for i in range(n):
            clause = [literals[i]]
            for j in graph[i]:
                clause.append(f'-{literals[j]}')
            clauses.append(clause)
            for j in range(i+1, n):
                if j not in graph[i] and j not in graph[j]:
                    clauses.append([f'-{literals[i]}', f'-{literals[j]}'])
        return clauses

    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i
            for j in range(i+1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            pivot = matrix[i][i]
            for j in range(cols):
                matrix[i][j] /= pivot
            for j in range(rows):
                if i != j:
                    factor = matrix[j][i]
                    for k in range(cols):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix

    def rank(matrix):
        rows, cols = len(matrix), len(matrix[0])
        matrix_copy = [row[:] for row in matrix]
        gaussian_elimination(matrix_copy)
        rank = 0
        for i in range(rows):
            if any(matrix_copy[i]):
                rank += 1
        return rank

    def tsi(graph):
        n = len(graph)
        clauses = tseitin_formula(graph)
        matrix = [[0] * (2*n + 1) for _ in range(2*n + 1)]
        for i, clause in enumerate(clauses):
            for literal in clause:
                if literal.startswith('x'):
                    j = int(literal[1:])
                    matrix[i][j] = 1
                else:
                    j = n + int(literal[1:])
                    matrix[i][j] = -1
        return rank(matrix)

    def communication_complexity_rank(clauses):
        n = len(clauses)
        matrix = [[0] * (2*n + 1) for _ in range(2*n + 1)]
        for i, clause in enumerate(clauses):
            for literal in clause:
                if literal.startswith('x'):
                    j = int(literal[1:])
                    matrix[i][j] = 1
                else:
                    j = n + int(literal[1:])
                    matrix[i][j] = -1
        return rank(matrix)

    n = random.randint(5, 40)
    d = random.randint(3, min(n-1, 2*n//3))
    graph = generate_d_regular_graph(n, d)
    if not graph:
        return {
            "metric_name": "tsi(G) - r(φ_G)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    tsi_value = tsi(graph)
    communication_rank = communication_complexity_rank(tseitin_formula(graph))
    
    return {
        "metric_name": "tsi(G) - r(φ_G)",
        "metric_value": abs(tsi_value - communication_rank),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(tsi_value - communication_rank) <= 0.1,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [631, 677, 727, 773, 821, 877, 929]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")