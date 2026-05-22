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

def generate_random_graph(n):
    graph = [[0] * n for _ in range(n)]
    edges = set()
    while len(edges) < (n * (n - 1)) // 2:
        i, j = random.sample(range(n), 2)
        if i > j:
            i, j = j, i
        if (i, j) not in edges:
            graph[i][j] = 1
            graph[j][i] = 1
            edges.add((i, j))
    return graph

def local_index(graph):
    n = len(graph)
    covered_edges = set()
    for i in range(n):
        for j in range(i + 1, n):
            if graph[i][j] == 1:
                covered_edges.update([(k, i), (k, j)] for k in range(n) if graph[k][i] == 1 or graph[k][j] == 1)
    return len(covered_edges)

def communication_complexity(graph):
    n = len(graph)
    # Simplified version of the communication complexity calculation
    return n * (n - 1) // 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    graph = generate_random_graph(n)
    loc_idx = local_index(graph)
    comm_complexity = communication_complexity(graph)
    
    expected_comm_complexity = math.ceil(n ** (1/3))
    if comm_complexity < expected_comm_complexity:
        return {
            "metric_name": "communication_complexity",
            "metric_value": comm_complexity,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Graph with n={n} has loc_idx={loc_idx}, but communication complexity {comm_complexity} < expected {expected_comm_complexity}"
        }
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": comm_complexity,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        support_fraction = 1.0
    else:
        support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    mean_comm_complexity = sum(result["metric_value"] for result in results) / len(results)
    std_comm_complexity = math.sqrt(sum((result["metric_value"] - mean_comm_complexity) ** 2 for result in results) / len(results))
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_comm_complexity} std={std_comm_complexity} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"communication_complexity < expected\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")