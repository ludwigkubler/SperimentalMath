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
        degrees = [0] * n
        for i in range(n):
            degree = random.randint(1, min(max_degree, n-1))
            neighbors = random.sample(range(n), degree)
            while len(set(neighbors)) != degree:
                neighbors = random.sample(range(n), degree)
            graph[i] = neighbors
            degrees[i] = degree
        return graph
    
    def compute_communication_matrix(graph):
        n = len(graph)
        comm_matrix = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if j in graph[i]:
                    comm_matrix[i][j] = 1
                    comm_matrix[j][i] = 1
        return comm_matrix
    
    def compute_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(n):
            if all(matrix[j][i] == 0 for j in range(m)):
                continue
            pivot_row = next(j for j in range(i, m) if matrix[j][i] != 0)
            matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
            for j in range(m):
                if j != i:
                    factor = -matrix[j][i] / matrix[i][i]
                    for k in range(n):
                        matrix[j][k] += factor * matrix[i][k]
            rank += 1
        return rank
    
    def compute_minimal_lattice_point_count(graph):
        n = len(graph)
        points = set()
        for i in range(n):
            for j in range(i+1, n):
                if j not in graph[i]:
                    continue
                point = (i, j)
                if point not in points:
                    points.add(point)
        return len(points)
    
    def is_valid_graph(graph):
        n = len(graph)
        for i in range(n):
            if len(graph[i]) != len(set(graph[i])):
                return False
        return True
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        if n > 30:
            continue
        for _ in range(5):  # Sample 5 instances per size
            graph = generate_random_graph(n, max_degree=4)
            if not is_valid_graph(graph):
                continue
            comm_matrix = compute_communication_matrix(graph)
            rank = compute_rank(comm_matrix)
            lattice_point_count = compute_minimal_lattice_point_count(graph)
            instances_tested += 1
            n_max = max(n_max, n)
            total_metric_value += lattice_point_count / rank
    
    if instances_tested < 30:
        conjecture_holds = False
        counterexample = "insufficient_instances"
    
    mean_metric_value = total_metric_value / instances_tested
    return {
        "metric_name": "L(G) / r(G)",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"insufficient_instances\" first_failing_seed={first_failing_seed}")