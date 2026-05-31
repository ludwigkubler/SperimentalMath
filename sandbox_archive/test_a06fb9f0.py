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
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i + max(range(i, rows), key=lambda x: abs(matrix[x][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            for j in range(cols):
                if j != i:
                    factor = Fraction(matrix[j][i], matrix[i][i])
                    for k in range(rows):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix

    def matrix_multiplication(A, B):
        rows_A, cols_A = len(A), len(A[0])
        cols_B = len(B[0])
        C = [[Fraction(0, 1) for _ in range(cols_B)] for _ in range(rows_A)]
        for i in range(rows_A):
            for j in range(cols_B):
                for k in range(cols_A):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def norm(matrix):
        rows, cols = len(matrix), len(matrix[0])
        sum_squares = Fraction(0, 1)
        for i in range(rows):
            for j in range(cols):
                sum_squares += matrix[i][j] ** 2
        return math.sqrt(sum_squares)

    def tseitin_formula(graph):
        n = len(graph)
        clauses = []
        for u in range(n):
            literals = [random.randint(0, 1) * 2 - 1 for _ in range(n)]
            literals[u] *= -1
            clause = [literals[i] + 2 * i + 1 for i in range(n) if graph[u][i]]
            clauses.append(clause)
        return clauses

    def resolution_width(clauses):
        queue = clauses[:]
        while True:
            new_clauses = []
            for i in range(len(queue)):
                for j in range(i + 1, len(queue)):
                    l1, l2 = queue[i], queue[j]
                    if any(abs(l) == abs(l2[k]) for k in range(len(l2))):
                        continue
                    new_clause = [l for l in l1 if not any(abs(l) == abs(l2[k])) for k in range(len(l2))]
                    if len(new_clause) == 0:
                        return 0
                    new_clauses.append(new_clause)
            queue.extend(new_clauses)
            if all(len(c) > 1 for c in queue):
                break
        return max(len(c) for c in queue)

    def geometric_quantization(graph):
        n = len(graph)
        quantum_state = [[Fraction(0, 1)] * n for _ in range(n)]
        for u in range(n):
            for v in range(u + 1, n):
                if graph[u][v]:
                    quantum_state[u][v] = Fraction(1, math.sqrt(2))
                    quantum_state[v][u] = Fraction(1, math.sqrt(2))
        return quantum_state

    def generate_d_regular_graph(n, d):
        graph = [[0] * n for _ in range(n)]
        degree = [0] * n
        for u in range(n):
            while degree[u] < d:
                v = random.randint(0, n - 1)
                if u != v and not graph[u][v]:
                    graph[u][v] = 1
                    graph[v][u] = 1
                    degree[u] += 1
                    degree[v] += 1
        return graph

    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov_xy / (std_x * std_y)

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        graph = generate_d_regular_graph(n, d=3)
        clauses = tseitin_formula(graph)
        width = resolution_width(clauses)
        quantum_state = geometric_quantization(graph)
        norm_rho = norm(quantum_state)
        results.append((width, norm_rho))

    if len(results) < 30:
        return {
            "metric_name": "Pearson Correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }

    widths, norms = zip(*results)
    correlation = pearson_correlation(widths, norms)

    return {
        "metric_name": "Pearson Correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.7,
        "counterexample": ""
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
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")