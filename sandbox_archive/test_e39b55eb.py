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
        if (n * d) % 2 != 0 or d < 1 or d >= n:
            return None
        adj_matrix = [[0] * n for _ in range(n)]
        edges_added = set()
        for i in range(n):
            neighbors = random.sample(range(n), d)
            for neighbor in neighbors:
                if (i, neighbor) not in edges_added and (neighbor, i) not in edges_added:
                    adj_matrix[i][neighbor] = 1
                    adj_matrix[neighbor][i] = 1
                    edges_added.add((i, neighbor))
        return adj_matrix
    
    def tseitin_formula(graph):
        n = len(graph)
        literals = [f'x{i}' for i in range(n)]
        clauses = []
        for i in range(n):
            clause = [literals[i]]
            for j in range(n):
                if graph[i][j] == 1:
                    clause.append(f'-{literals[j]}')
            clauses.append(clause)
        for i in range(n):
            for j in range(i + 1, n):
                clauses.append([f'-{literals[i]}', f'-{literals[j]}'])
                clauses.append([f'{literals[i]}', f'{literals[j]}'])
        return clauses
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            if matrix[i][i] == 0:
                for j in range(i + 1, n):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        break
                else:
                    return None
            pivot = matrix[i][i]
            for j in range(n):
                matrix[i][j] /= pivot
            for j in range(n):
                if j == i:
                    continue
                factor = matrix[j][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def minimal_tropical_motivic_rank(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if all(row[i] == 0 for row in matrix):
                continue
            rank += 1
            pivot_row = [matrix[j][i] for j in range(n)]
            for j in range(n):
                if j != i:
                    factor = matrix[j][i]
                    for k in range(n):
                        matrix[j][k] -= factor * pivot_row[k]
        return rank
    
    def resolution_width(clauses):
        n = len(clauses)
        queue = clauses[:]
        learned_clauses = []
        while queue:
            clause = queue.pop(0)
            if not any(lit[0] == '-' for lit in clause):
                return len(queue) + 1
            unit_clause = next((lit for lit in clause if lit[0] != '-'), None)
            if unit_clause is None:
                break
            learned_clauses.append([f'-{unit_clause}'])
            queue.extend(clause for clause in clauses if any(lit == f'-{unit_clause}' or lit == unit_clause for lit in clause))
        return len(queue) + 1
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        var_x = sum((x[i] - mean_x) ** 2 for i in range(n)) / n
        var_y = sum((y[i] - mean_y) ** 2 for i in range(n)) / n
        return cov_xy / (math.sqrt(var_x) * math.sqrt(var_y))
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        mtr_values = []
        width_values = []
        for _ in range(5):
            graph = generate_d_regular_graph(n, random.randint(2, n - 1))
            if graph is None:
                continue
            phi = tseitin_formula(graph)
            mtr = minimal_tropical_motivic_rank(gaussian_elimination(phi))
            width = resolution_width(phi)
            if mtr is not None and width is not None:
                mtr_values.append(mtr)
                width_values.append(width)
        if len(mtr_values) < 3 or len(width_values) < 3:
            continue
        correlation = pearson_correlation(mtr_values, width_values)
        results.append(correlation)
    
    mean_corr = sum(results) / len(results)
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": mean_corr,
        "instances_tested": len(results),
        "n_max": max(n for n in [5, 10, 15, 20, 30, 40] if any(len(mtr_values) > 0 for mtr_values in results)),
        "conjecture_holds": mean_corr >= 0.5,
        "counterexample": "" if mean_corr >= 0.5 else f"Correlation < 0.2: {mean_corr}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean_corr = sum(results) / len(results)
    support_fraction = sum(1 for r in results if r >= 0.5) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std={math.sqrt(sum((r - mean_corr) ** 2 for r in results) / len(results))} support_fraction={support_fraction}")
    elif any(r < 0.2 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result < 0.2)
        print(f"RESULT: FALSIFIED counterexample='Correlation < 0.2' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")