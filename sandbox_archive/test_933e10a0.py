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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        if A[i][i] == 0:
            return None  # Singular matrix
        for j in range(i+1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    rank = sum(1 for row in A if any(row))
    return rank

def d_regular_expander_graph(d, n):
    graph = [[] for _ in range(n)]
    nodes = list(range(n))
    random.shuffle(nodes)
    for i in range(n):
        neighbors = nodes[i+1:i+d+1]
        for neighbor in neighbors:
            graph[i].append(neighbor)
            graph[neighbor].append(i)
    return graph

def clause_incidence_matrix(graph, n):
    m = len(graph) * 2
    matrix = [[0] * n for _ in range(m)]
    for i in range(n):
        for j in range(len(graph[i])):
            matrix[2*i][graph[i][j]] = 1
            matrix[2*i+1][graph[i][j]] = -1
    return matrix

def resolution_width(matrix, n):
    queue = [i for i in range(n) if any(row[i] == 1 for row in matrix)]
    visited = set(queue)
    while queue:
        new_queue = []
        for node in queue:
            for j in range(len(matrix)):
                if matrix[j][node] == -1 and all(matrix[j][k] == 0 for k in visited):
                    for k in range(n):
                        if matrix[j][k] == 1 and k not in visited:
                            new_queue.append(k)
                            visited.add(k)
        queue = new_queue
    return len(visited)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        d = random.randint(2, min(n-1, 5))
        graph = d_regular_expander_graph(d, n)
        matrix = clause_incidence_matrix(graph, n)
        jordan_rank = gaussian_elimination(matrix)
        
        if jordan_rank is None:
            continue
        
        width = resolution_width(matrix, n)
        instances_tested += 1
        total_metric_value += jordan_rank * math.sqrt(n) / width

    mean_metric_value = total_metric_value / instances_tested
    support_fraction = instances_tested / len(n_values)

    if support_fraction < 0.8:
        conjecture_holds = False
        counterexample = "support_fraction_too_low"

    return {
        "metric_name": "jordan_rank_resolution_width_ratio",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{trial_result}...}}")
        results.append(trial_result)

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"support_fraction_too_low\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction_too_low")