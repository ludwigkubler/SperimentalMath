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
        if d * n % 2 != 0:
            return None
        graph = {i: [] for i in range(n)}
        edges_added = set()
        while len(edges_added) < (d * n) // 2:
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u != v and (u, v) not in edges_added and (v, u) not in edges_added:
                graph[u].append(v)
                graph[v].append(u)
                edges_added.add((u, v))
        return graph
    
    def compute_clause_set(graph):
        clause_set = []
        for node in graph:
            for neighbor in graph[node]:
                if node < neighbor:
                    clause_set.append([node + 1, -neighbor - 1])
        return clause_set
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(n):
            pivot_row = None
            for j in range(rank, m):
                if matrix[j][i] != 0:
                    pivot_row = j
                    break
            if pivot_row is None:
                continue
            matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
            for j in range(m):
                if j != rank and matrix[j][i] != 0:
                    factor = -matrix[j][i] / matrix[rank][i]
                    for k in range(n):
                        matrix[j][k] += factor * matrix[rank][k]
            rank += 1
        return rank
    
    def compute_noncommutative_crossed_product_order(clause_set):
        n = len(clause_set)
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for i, clause in enumerate(clause_set):
            for var in clause:
                if var > 0:
                    matrix[i][var - 1] += 1
                else:
                    matrix[var - 1][i] += 1
        return gaussian_elimination(matrix)
    
    def compute_resolution_proof_width(clause_set):
        stack = []
        for clause in clause_set:
            if not any(var in stack for var in clause):
                stack.append(random.choice(clause))
        return len(stack)
    
    n_max = 0
    instances_tested = 0
    total_order = 0
    total_width = 0
    
    for _ in range(30):
        d = random.randint(2, 40)
        n = (d * n) // 2 + 1
        if n > n_max:
            n_max = n
        graph = generate_d_regular_graph(d, n)
        if graph is None:
            continue
        clause_set = compute_clause_set(graph)
        order = compute_noncommutative_crossed_product_order(clause_set)
        width = compute_resolution_proof_width(clause_set)
        total_order += order
        total_width += width
        instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_order = total_order / instances_tested
    mean_width = total_width / instances_tested
    
    correlation = (sum((order - mean_order) * (width - mean_width) for order, width in zip(clause_set, clause_set)) /
                   math.sqrt(sum((order - mean_order) ** 2 for order in clause_set) *
                             sum((width - mean_width) ** 2 for width in clause_set)))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation) >= 0.5,  # Threshold for linear correlation
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(2, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")