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
    
    def generate_k_colorable_graph(n, k):
        if n < k or k <= 1:
            return None
        colors = list(range(k))
        graph = [[] for _ in range(n)]
        nodes = list(range(n))
        random.shuffle(nodes)
        for i in range(n - 1):
            node = nodes[i]
            color = random.choice(colors)
            other_nodes = [n for n in nodes if n != node and len(graph[n]) < k - 1]
            if not other_nodes:
                break
            other_node = random.choice(other_nodes)
            graph[node].append(other_node)
            graph[other_node].append(node)
        return graph
    
    def compute_brauer_classes(graph):
        if not graph:
            return 0
        n = len(graph)
        edges = [(i, j) for i in range(n) for j in range(i + 1, n) if j in graph[i]]
        if not edges:
            return 1
        field_size = 2
        while True:
            field = [Fraction(0)] * (field_size ** len(edges))
            valid = True
            for i, (u, v) in enumerate(edges):
                for j in range(field_size):
                    for k in range(field_size):
                        if not (field[j * field_size + k] == Fraction(0)):
                            continue
                        new_field = field[:]
                        new_field[j * field_size + k] = Fraction(1)
                        valid = True
                        for l in range(len(edges)):
                            if i != l:
                                u2, v2 = edges[l]
                                if (u == u2 and v == v2) or (u == v2 and v == u2):
                                    continue
                                a = new_field[j * field_size + k] * Fraction(1)
                                b = new_field[j * field_size + k] * Fraction(-1)
                                c = new_field[j * field_size + k] * Fraction(0)
                                d = new_field[j * field_size + k] * Fraction(0)
                                if not (a == b or c == d):
                                    valid = False
                                    break
                            if not valid:
                                break
                        if not valid:
                            break
                    if not valid:
                        break
                if not valid:
                    break
            if valid:
                return field_size
            field_size += 1
    
    def compute_communication_rank(graph):
        n = len(graph)
        if n == 0:
            return 0
        rank = 1
        visited = [False] * n
        queue = [0]
        while queue:
            node = queue.pop(0)
            if not visited[node]:
                visited[node] = True
                for neighbor in graph[node]:
                    if not visited[neighbor]:
                        queue.append(neighbor)
                        rank += 1
        return rank
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        var_x = sum((x[i] - mean_x) ** 2 for i in range(n)) / n
        var_y = sum((y[i] - mean_y) ** 2 for i in range(n)) / n
        return cov_xy / (math.sqrt(var_x) * math.sqrt(var_y))
    
    k = random.randint(3, 5)
    br_values = []
    comm_rank_values = []
    instances_tested = 0
    n_max = 1
    
    for n in [5, 10, 15, 20, 30, 40]:
        if instances_tested >= 30:
            break
        graph = generate_k_colorable_graph(n, k)
        if not graph:
            continue
        br_value = compute_brauer_classes(graph)
        comm_rank_value = compute_communication_rank(graph)
        if br_value is None or comm_rank_value is None:
            continue
        br_values.append(br_value)
        comm_rank_values.append(comm_rank_value)
        instances_tested += 1
        n_max = max(n_max, n)
    
    if not br_values or not comm_rank_values:
        return {
            "metric_name": "Pearson's r",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation = pearson_correlation(br_values, comm_rank_values)
    return {
        "metric_name": "Pearson's r",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"n={r['instances_tested']}, br(G)={r['metric_value']}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break