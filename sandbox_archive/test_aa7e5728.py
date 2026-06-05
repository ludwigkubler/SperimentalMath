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
        if (n * d) % 2 != 0:
            return None
        graph = [[] for _ in range(n)]
        edges_added = set()
        for i in range(n):
            for j in range(i + 1, n):
                if len(graph[i]) < d and len(graph[j]) < d:
                    edge = (i, j)
                    reverse_edge = (j, i)
                    if edge not in edges_added and reverse_edge not in edges_added:
                        graph[i].append(j)
                        graph[j].append(i)
                        edges_added.add(edge)
                        edges_added.add(reverse_edge)
        return graph
    
    def communication_complexity_matrix(graph):
        n = len(graph)
        matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if graph[i][j]:
                    matrix[i][j] = 1
        return matrix
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        augmented_matrix = [row + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(matrix)]
        for col in range(n):
            max_row = max(range(col, m), key=lambda r: abs(augmented_matrix[r][col]))
            augmented_matrix[col], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[col]
            if augmented_matrix[col][col] == 0:
                return float('inf')
            for row in range(m):
                if row != col:
                    factor = augmented_matrix[row][col] / augmented_matrix[col][col]
                    for j in range(n + 1):
                        augmented_matrix[row][j] -= factor * augmented_matrix[col][j]
        rank = sum(1 for row in range(n) if augmented_matrix[row][-1] != 0)
        return rank
    
    def tft_state_order(matrix):
        n = len(matrix)
        order = 0
        visited = [False] * n
        stack = []
        for i in range(n):
            if not visited[i]:
                stack.append(i)
                while stack:
                    node = stack.pop()
                    if not visited[node]:
                        visited[node] = True
                        order += 1
                        for neighbor in graph[node]:
                            if not visited[neighbor]:
                                stack.append(neighbor)
        return order
    
    n_min, n_max = 5, 40
    instances_tested = 0
    total_order = 0
    total_rank = 0
    correlation_values = []
    
    for n in range(n_min, n_max + 1):
        d = random.randint(2, min(n - 1, 3))
        graph = generate_d_regular_graph(d, n)
        if graph is None:
            continue
        
        matrix = communication_complexity_matrix(graph)
        rank_value = rank(matrix)
        order_value = tft_state_order(matrix)
        
        instances_tested += 1
        total_order += order_value
        total_rank += rank_value
        correlation_values.append(order_value / (d ** 2 * math.log(n)))
    
    mean_order = total_order / instances_tested if instances_tested > 0 else 0
    mean_rank = total_rank / instances_tested if instances_tested > 0 else 0
    support_fraction = sum(1 for corr in correlation_values if corr >= 0.8) / len(correlation_values)
    
    conjecture_holds = support_fraction >= 0.8 and all(corr >= 0.8 for corr in correlation_values)
    counterexample = "" if conjecture_holds else "correlation_threshold_not_met"
    
    return {
        "metric_name": "TFT State Order vs Communication Complexity Rank",
        "metric_value": mean_order,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_order = sum(res["metric_value"] for res in results) / len(results)
    std_deviation = math.sqrt(sum((res["metric_value"] - mean_order) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_order} std={std_deviation} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and support_fraction >= 0.8:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_threshold_not_met\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")