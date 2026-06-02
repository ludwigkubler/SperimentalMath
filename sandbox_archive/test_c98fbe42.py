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
                    for k in range(cols):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix

    def matrix_multiply(A, B):
        rows_A, cols_A = len(A), len(A[0])
        cols_B = len(B[0])
        result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
        for i in range(rows_A):
            for j in range(cols_B):
                for k in range(cols_A):
                    result[i][j] += A[i][k] * B[k][j]
        return result

    def determinant(matrix):
        if len(matrix) == 1:
            return matrix[0][0]
        det = Fraction(0)
        sign = 1
        for j in range(len(matrix[0])):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += sign * matrix[0][j] * determinant(submatrix)
            sign *= -1
        return det

    def find_algebraic_curves(graph):
        n = len(graph)
        max_independent_set_size = 0
        for i in range(1, 2**n):
            independent_set = [j for j in range(n) if (i & (1 << j))]
            if all(node not in graph[neighbor] for node in independent_set for neighbor in independent_set):
                max_independent_set_size = max(max_independent_set_size, len(independent_set))
        return max_independent_set_size

    def geometric_entropy(curves):
        n = len(curves)
        if n == 0:
            return 0
        entropy = 0
        for i in range(n):
            for j in range(i+1, n):
                if curves[i] != curves[j]:
                    entropy += 1
        return entropy

    def communication_complexity_rank(graph):
        n = len(graph)
        rank = 0
        for i in range(1, 2**n):
            independent_set = [j for j in range(n) if (i & (1 << j))]
            subgraph = {node: set() for node in independent_set}
            for u, v in graph.items():
                if u in independent_set and v in independent_set:
                    subgraph[u].add(v)
            rank = max(rank, len(find_algebraic_curves(subgraph)))
        return rank

    def generate_random_graph(n):
        graph = {i: set() for i in range(n)}
        edges = random.randint(0, n*(n-1)//2)
        for _ in range(edges):
            u, v = random.sample(range(n), 2)
            if u != v and v not in graph[u]:
                graph[u].add(v)
                graph[v].add(u)
        return graph

    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        graph = generate_random_graph(n)
        rank = communication_complexity_rank(graph)
        curves = find_algebraic_curves(graph)
        entropy = geometric_entropy(curves)

        total_metric_value += entropy
        instances_tested += 1
        n_max = max(n_max, n)

        if entropy > 10:
            conjecture_holds = False
            counterexample = f"n={n}, rank={rank}, entropy={entropy}"

    return {
        "metric_name": "geometric_entropy",
        "metric_value": total_metric_value / instances_tested,
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

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] and r["counterexample"] != "" for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")