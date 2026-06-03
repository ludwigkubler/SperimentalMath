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
        if (n * d) % 2 != 0:
            return None
        graph = [[] for _ in range(n)]
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
        literals = [f'x{i}' for i in range(n)]
        clauses = []
        for i in range(n):
            clause = [literals[i]]
            for j in graph[i]:
                clause.append(f'-{literals[j]}')
            clauses.append(clause)
        for i in range(n):
            for j in range(i + 1, n):
                clauses.append([f'-{literals[i]}', f'-{literals[j]}'])
                clauses.append([f'{literals[i]}', f'{literals[j]}'])
        return literals, clauses
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i
            for j in range(i + 1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            pivot = matrix[i][i]
            for j in range(cols):
                matrix[i][j] /= pivot
            for j in range(rows):
                if j != i:
                    factor = matrix[j][i]
                    for k in range(cols):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def tropical_analytic_rank(matrix):
        n = len(matrix)
        max_plus_matrix = [[float('-inf')] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if matrix[i][j] != float('inf'):
                    max_plus_matrix[i][j] = max(matrix[i][j], matrix[j][i])
        return gaussian_elimination(max_plus_matrix)
    
    def resolution_proof_width(clauses):
        n = len(clauses)
        clauses = [sorted(c) for c in clauses]
        clauses.sort(key=lambda x: (-len(x), x))
        queue = []
        for clause in clauses:
            if not any(lit in queue for lit in clause):
                queue.append(clause[0])
        while queue:
            literal = queue.pop()
            new_clauses = []
            for clause in clauses:
                if literal in clause:
                    continue
                if -literal in clause:
                    return len(queue)
                new_clause = [lit for lit in clause if lit != -literal]
                if new_clause and all(lit not in queue for lit in new_clause):
                    new_clauses.append(new_clause)
            clauses = new_clauses
        return len(queue)
    
    def linear_regression(x, y):
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_xx = sum(xi ** 2 for xi in x)
        b1 = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x ** 2)
        b0 = (sum_y - b1 * sum_x) / n
        return b0, b1
    
    def solve(lits_true, lits_false):
        queue = []
        for lit in lits_true:
            if lit not in queue:
                queue.append(lit)
        while queue:
            literal = queue.pop()
            new_clauses = []
            for clause in clauses:
                if literal in clause:
                    continue
                if -literal in clause:
                    return False
                new_clause = [lit for lit in clause if lit != -literal]
                if new_clause and all(lit not in queue for lit in new_clause):
                    new_clauses.append(new_clause)
            clauses = new_clauses
        return True
    
    n_values = [10, 15, 20, 25, 30, 35, 40]
    ratios = []
    
    for n in n_values:
        graph = generate_d_regular_graph(n, 3)
        if not graph:
            continue
        literals, clauses = tseitin_formula(graph)
        tar_matrix = tropical_analytic_rank([[float('inf')] * n for _ in range(n)])
        tar_value = sum(1 for row in tar_matrix if any(x != float('-inf') for x in row))
        w_value = resolution_proof_width(clauses)
        ratios.append(tar_value / w_value)
    
    if not ratios:
        return {
            "metric_name": "tropical_analytic_rank_over_resolution_width",
            "metric_value": 0.0,
            "instances_tested": len(n_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_ratio = sum(ratios) / len(ratios)
    std_ratio = math.sqrt(sum((r - mean_ratio) ** 2 for r in ratios) / len(ratios))
    if all(r <= 10 for r in ratios):
        return {
            "metric_name": "tropical_analytic_rank_over_resolution_width",
            "metric_value": mean_ratio,
            "instances_tested": len(n_values),
            "n_max": max(n_values),
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "tropical_analytic_rank_over_resolution_width",
            "metric_value": mean_ratio,
            "instances_tested": len(n_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": f"ratio > 10 at n={max(n for n, r in zip(n_values, ratios) if r > 10)}"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")