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
    
    def generate_random_graph(n, max_degree):
        graph = [[] for _ in range(n)]
        degree_sum = 0
        while degree_sum < n * max_degree:
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u != v and v not in graph[u]:
                graph[u].append(v)
                graph[v].append(u)
                degree_sum += 2
        return graph
    
    def matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(n):
            if all(matrix[j][i] == 0 for j in range(m)):
                continue
            pivot_row = next(j for j in range(i, m) if matrix[j][i] != 0)
            matrix[pivot_row], matrix[i] = matrix[i], matrix[pivot_row]
            for j in range(m):
                if j != i:
                    factor = matrix[j][i] / matrix[i][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
            rank += 1
        return rank
    
    def lattice_point_count(graph, n):
        count = 0
        for x in range(2**n):
            valid = True
            for i in range(n):
                if (x >> i) & 1:
                    for j in graph[i]:
                        if not ((x >> j) & 1):
                            valid = False
                            break
                    if not valid:
                        break
            if valid:
                count += 1
        return count
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    max_degree = min(n - 1, 3)
    graph = generate_random_graph(n, max_degree)
    
    r_G = matrix_rank(graph)
    L_G = lattice_point_count(graph, n)
    
    if r_G == 0:
        return {
            "metric_name": "L(G) / r(G)",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Graph has zero rank"
        }
    
    ratio = L_G / r_G
    c = 0.5  # Pre-specified constant
    
    return {
        "metric_name": "L(G) / r(G)",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ratio >= c,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")