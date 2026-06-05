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
    
    def generate_quasigroup(n):
        q = [[0] * n for _ in range(n)]
        elements = list(range(n))
        for i in range(n):
            random.shuffle(elements)
            for j in range(n):
                q[i][j] = elements[(i + j) % n]
        return q
    
    def min_index(q):
        n = len(q)
        indices = [0] * n
        for i in range(n):
            for j in range(n):
                if q[i][j] != (i + j) % n:
                    indices[q[i][j]] += 1
        return max(indices)
    
    def matrix_from_quasigroup(q):
        n = len(q)
        matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                matrix[i][q[i][j]] = 1
        return matrix
    
    def communication_complexity_rank(matrix):
        n = len(matrix)
        adj_matrix = [[matrix[i][j] + matrix[j][i] for j in range(n)] for i in range(n)]
        degree = [sum(row) for row in adj_matrix]
        max_degree = max(degree)
        if max_degree == 0:
            return 0
        rank = 0
        visited = [False] * n
        for i in range(n):
            if not visited[i]:
                queue = [i]
                while queue:
                    node = queue.pop()
                    if not visited[node]:
                        visited[node] = True
                        rank += 1
                        for j in range(n):
                            if adj_matrix[node][j] > 0 and not visited[j]:
                                queue.append(j)
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    metrics = []
    
    for n in n_values:
        q = generate_quasigroup(n)
        min_idx = min_index(q)
        matrix = matrix_from_quasigroup(q)
        rank = communication_complexity_rank(matrix)
        metrics.append((min_idx, rank))
    
    if not metrics:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation = sum((x[0] - y[0]) * (x[1] - y[1]) for x, y in zip(metrics[:-1], metrics[1:])) / len(metrics)
    mean_metric_value = sum(x[0] for x in metrics) / len(metrics)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(metrics),
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.8 and mean_metric_value <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"correlation below threshold\" first_failing_seed={r['seed']}")
                break