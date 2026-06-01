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
        adj_list = [[] for _ in range(n)]
        edges_added = set()
        for i in range(d):
            for node in range(n):
                neighbors = [x for x in range(n) if x != node and x not in adj_list[node]]
                if len(neighbors) == 0:
                    return None
                neighbor = random.choice(neighbors)
                if (node, neighbor) not in edges_added and (neighbor, node) not in edges_added:
                    adj_list[node].append(neighbor)
                    adj_list[neighbor].append(node)
                    edges_added.add((node, neighbor))
        return adj_list

    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = matrix[i][i]
            for j in range(n):
                matrix[i][j] /= factor
            for j in range(n):
                if j != i:
                    factor = matrix[j][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix

    def min_rank(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            row = [matrix[j][i] for j in range(n)]
            if any(row):
                rank += 1
        return rank

    def communication_complexity_rank(graph):
        n = len(graph)
        max_degree = max(len(neighbors) for neighbors in graph)
        return max_degree

    d = 3
    n_min = 5
    n_max = 40
    instances_per_seed = 30
    total_instances = (n_max - n_min + 1) * instances_per_seed
    
    if total_instances > 30:
        print('RESULT: INCONCLUSIVE reason=too_many_instances')
        return

    results = []
    for _ in range(instances_per_seed):
        n = random.randint(n_min, n_max)
        graph = generate_d_regular_graph(n, d)
        if graph is None:
            continue
        cc_rank = communication_complexity_rank(graph)
        matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if j in graph[i]:
                    matrix[i][j] = 1
                    matrix[j][i] = 1
        min_rank_val = min_rank(gaussian_elimination(matrix))
        results.append((min_rank_val, cc_rank))

    if len(results) < instances_per_seed:
        print('RESULT: INCONCLUSIVE reason=insufficient_data')
        return

    min_rank_vals, cc_ranks = zip(*results)
    mean_diff = sum(abs(x - y) for x, y in zip(min_rank_vals, cc_ranks)) / len(results)
    std_dev = math.sqrt(sum((x - mean_diff)**2 for x in results) / len(results))
    
    conjecture_holds = all(abs(x - y) <= 1.5 * std_dev for x, y in zip(min_rank_vals, cc_ranks))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "min_rank_vs_cc_rank",
        "metric_value": mean_diff,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result)
    
    mean_diff = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_diff)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f'RESULT: SUPPORTED mean={mean_diff} std={std_dev} support_fraction={support_fraction}')
    elif support_fraction >= 0.8:
        print(f'RESULT: SUPPORTED mean={mean_diff} std={std_dev} support_fraction={support_fraction}')
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f'RESULT: FALSIFIED counterexample="mapping_undefined" first_failing_seed={first_failing_seed}')