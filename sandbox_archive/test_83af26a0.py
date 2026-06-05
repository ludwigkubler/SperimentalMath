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
        if (n * d) % 2 != 0:
            return None
        graph = [[] for _ in range(n)]
        edges_added = set()
        for i in range(d // 2):
            for j in range(i + 1, n):
                if len(graph[i]) < d and len(graph[j]) < d:
                    if (i, j) not in edges_added and (j, i) not in edges_added:
                        graph[i].append(j)
                        graph[j].append(i)
                        edges_added.add((i, j))
                        edges_added.add((j, i))
        return graph
    
    def communication_complexity_rank(graph):
        n = len(graph)
        rank = 0
        for node in range(n):
            rank += len(graph[node])
        return rank // n
    
    def minimal_order_of_representations(graph):
        n = len(graph)
        if n == 1:
            return 1
        adjacency_matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in graph[i]:
                adjacency_matrix[i][j] = 1
        
        def gaussian_elimination(matrix):
            rows, cols = len(matrix), len(matrix[0])
            rank = 0
            for col in range(cols):
                pivot_row = -1
                for row in range(rank, rows):
                    if matrix[row][col] != 0:
                        pivot_row = row
                        break
                if pivot_row == -1:
                    continue
                matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
                rank += 1
                for row in range(rank, rows):
                    factor = matrix[row][col] / matrix[pivot_row][col]
                    for j in range(cols):
                        matrix[row][j] -= factor * matrix[pivot_row][j]
            return rank
        
        rank = gaussian_elimination(adjacency_matrix)
        return n - rank
    
    def is_valid_graph(graph, d):
        n = len(graph)
        if (n * d) % 2 != 0:
            return False
        for node in range(n):
            if len(graph[node]) != d:
                return False
        return True
    
    instances_tested = 0
    mqr_sum = 0
    r_sum = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            d = random.randint(2, min(n - 1, 4))
            graph = generate_d_regular_graph(n, d)
            if not is_valid_graph(graph, d):
                continue
            instances_tested += 1
            mqr = minimal_order_of_representations(graph)
            r = communication_complexity_rank(graph)
            mqr_sum += mqr
            r_sum += r
            n_max = max(n_max, n)
            if mqr < r:
                conjecture_holds = False
                counterexample = f"Graph with n={n}, d={d} has mqr(G)={mqr} < r(G)={r}"
    
    metric_value = mqr_sum / instances_tested
    return {
        "metric_name": "mqr/G",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(sys.argv[1])] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unsupported_group_size")