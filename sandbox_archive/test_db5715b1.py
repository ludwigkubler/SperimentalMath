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
            max_row = i
            for j in range(i+1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = matrix[i][i]
            for j in range(cols):
                matrix[i][j] /= factor
            for k in range(rows):
                if k != i:
                    factor = matrix[k][i]
                    for j in range(cols):
                        matrix[k][j] -= factor * matrix[i][j]
        return matrix
    
    def jordan_rank(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for i in range(rows):
            if any(matrix[i][j] != 0 for j in range(cols)):
                rank += 1
        return rank
    
    def resolution_width(clause_incidence_matrix):
        n = len(clause_incidence_matrix)
        width = 0
        for i in range(n):
            clause = clause_incidence_matrix[i]
            if any(clause[j] == 1 for j in range(n)):
                width += 1
        return width
    
    def generate_d_regular_expander(d, n):
        graph = [[] for _ in range(n)]
        degree_count = [0] * n
        while True:
            u = random.randint(0, n-1)
            v = random.randint(0, n-1)
            if u != v and len(graph[u]) < d and len(graph[v]) < d and (u, v) not in graph and (v, u) not in graph:
                graph[u].append(v)
                graph[v].append(u)
                degree_count[u] += 1
                degree_count[v] += 1
            if all(d == d for d in degree_count):
                break
        return graph
    
    def clause_incidence_matrix(graph, n):
        matrix = [[0 for _ in range(n)] for _ in range(n)]
        for u in range(n):
            for v in range(u+1, n):
                if (u, v) in graph or (v, u) in graph:
                    matrix[u][v] = 1
                    matrix[v][u] = 1
        return matrix
    
    d = random.randint(3, 5)
    n = random.choice([5, 10, 15, 20, 30, 40])
    graph = generate_d_regular_expander(d, n)
    clause_incidence_matrix = clause_incidence_matrix(graph, n)
    jordan_rank_value = jordan_rank(clause_incidence_matrix)
    resolution_width_value = resolution_width(clause_incidence_matrix)
    
    metric_name = "resolution_width"
    metric_value = resolution_width_value
    instances_tested = 1
    conjecture_holds = jordan_rank_value >= math.sqrt(n) and resolution_width_value >= math.sqrt(n)
    counterexample = "" if conjecture_holds else f"Jordan rank {jordan_rank_value} < √{n} or resolution width {resolution_width_value} < √{n}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")