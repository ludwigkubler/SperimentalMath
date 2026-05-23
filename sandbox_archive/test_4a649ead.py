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
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i + max(range(i, rows), key=lambda j: abs(matrix[j][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = 1 / matrix[i][i]
            for j in range(cols):
                matrix[i][j] *= factor
            for k in range(rows):
                if k != i:
                    factor = matrix[k][i]
                    for j in range(cols):
                        matrix[k][j] -= factor * matrix[i][j]
        return matrix

    def rank(matrix):
        reduced_matrix = gaussian_elimination(matrix)
        rank = 0
        for row in reduced_matrix:
            if any(row):
                rank += 1
        return rank

    def tseitin_formula(graph):
        n = len(graph)
        clauses = []
        for i in range(n):
            clauses.append([i + 1, -n - i - 1])
            for j in range(i + 1, n):
                if graph[i][j]:
                    clauses.append([-i - 1, -j - 1, i + j + 2])
        return clauses

    def resolution_length(clauses):
        queue = set(clauses)
        while True:
            new_clauses = []
            for clause1 in queue:
                for clause2 in queue:
                    if len(set(clause1) & set(clause2)) == 1:
                        new_clause = list(set(clause1) ^ set(clause2))
                        if not any(new_clause == clause for clause in queue):
                            new_clauses.append(new_clause)
            if not new_clauses:
                break
            queue.update(new_clauses)
        return len(queue)

    def generate_random_graph(n):
        graph = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    graph[i][j] = graph[j][i] = 1
        return graph

    def mean(lst):
        return sum(lst) / len(lst)

    def std(lst):
        avg = mean(lst)
        return math.sqrt(sum((x - avg) ** 2 for x in lst) / len(lst))

    n = random.choice([5, 10, 15, 20, 30, 40])
    graph = generate_random_graph(n)
    config_space_rank = rank(graph)
    tseitin_clauses = tseitin_formula(graph)
    resolution_len = resolution_length(tseitin_clauses)

    metric_name = "Resolution Proof Length"
    metric_value = resolution_len
    instances_tested = 1
    conjecture_holds = resolution_len >= 2 ** (0.5 * config_space_rank)
    counterexample = "" if conjecture_holds else f"Graph with n={n}, rank(C(G))={config_space_rank}, Tseitin length={resolution_len}"

    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
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

    mean_value = mean([r["metric_value"] for r in results])
    std_value = std([r["metric_value"] for r in results])
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Graph with n={n}, rank(C(G))={config_space_rank}, Tseitin length={resolution_len}\" first_failing_seed={first_failing_seed}")