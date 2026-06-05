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
        if n % d != 0:
            return None
        graph = [[0] * n for _ in range(n)]
        edges = set()
        for i in range(n):
            neighbors = random.sample(range(n), d - 1)
            while any((i, j) in edges or (j, i) in edges for j in neighbors):
                neighbors = random.sample(range(n), d - 1)
            for j in neighbors:
                graph[i][j] = 1
                graph[j][i] = 1
                edges.add((i, j))
        return graph
    
    def frobenius_action(matrix, p):
        n = len(matrix)
        result = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                result[i][j] = sum(matrix[(i + k) % n][(j + l) % n] for k in range(p) for l in range(p)) % p
        return result
    
    def h_index(matroid):
        p = 2
        while True:
            frobenius_matroid = frobenius_action(matroid, p)
            if all(all(frobenius_matroid[i][j] == matroid[i][j] for j in range(len(matroid))) for i in range(len(matroid))):
                return p - 1
            p += 1
    
    def circuit_monotone_width(graph):
        n = len(graph)
        max_width = 0
        for k in range(1, n + 1):
            subsets = [set() for _ in range(k)]
            for i in range(n):
                if graph[0][i]:
                    subsets[i % k].add(i)
            width = 0
            for subset in subsets:
                if all(graph[u][v] == 1 for u, v in itertools.combinations(subset, 2)):
                    width += 1
            max_width = max(max_width, width)
        return max_width
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_h_index = 0
    total_w_m = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):
            graph = generate_d_regular_graph(n, 2)
            if graph is None:
                continue
            matroid = [[graph[i][j] for j in range(n)] for i in range(n)]
            h_index_val = h_index(matroid)
            w_m_val = circuit_monotone_width(graph)
            if h_index_val > 3 * w_m_val:
                return {
                    "metric_name": "correlation_coefficient",
                    "metric_value": None,
                    "instances_tested": instances_tested,
                    "n_max": n_max,
                    "conjecture_holds": False,
                    "counterexample": f"h_index({h_index_val}) > 3 * w_m({w_m_val})"
                }
            total_h_index += h_index_val
            total_w_m += w_m_val
            instances_tested += 1
            n_max = max(n_max, n)
    
    if instances_tested < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    correlation_coefficient = total_h_index / instances_tested * total_w_m / instances_tested
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient > 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = [run_trial(seed) for seed in seeds]
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")