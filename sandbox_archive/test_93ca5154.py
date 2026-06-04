# auto-injected by SEC sandbox
import itertools
import collections
import json
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
import sys

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def nearest_neighbor_graph(boolean_function, n):
    graph = {}
    for i in range(2**n):
        distances = []
        for j in range(i + 1, 2**n):
            hamming_distance = sum(x != y for x, y in zip(bin(i)[2:].zfill(n), bin(j)[2:].zfill(n)))
            distances.append((j, hamming_distance))
        graph[i] = sorted(distances, key=lambda x: x[1])
    return graph

def geometric_entropy(graph, n):
    total_distance = 0
    count = 0
    for i in range(2**n):
        for j, distance in graph[i]:
            if distance > 0:
                total_distance += math.log(distance)
                count += 1
    if count == 0:
        return 0
    average_distance = total_distance / count
    return -average_distance

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        # Find the pivot row
        max_row = i
        for j in range(i + 1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        # Swap rows
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate non-pivot elements
        for j in range(i + 1, n):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(n + 1):
                matrix[j][k] -= factor * matrix[i][k]
    
    rank = sum(1 for row in matrix if any(row))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        boolean_function = generate_boolean_function(n)
        graph = nearest_neighbor_graph(boolean_function, n)
        g_ent = geometric_entropy(graph, n)
        
        # Compute communication complexity matrix
        matrix = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(i + 1, 2**n):
                if graph[i][j][1] == 1:
                    matrix[i][j] = 1
                    matrix[j][i] = 1
        
        rank = gaussian_elimination(matrix)
        
        results.append({
            "n": n,
            "g_ent": g_ent,
            "rank": rank
        })
    
    instances_tested = len(results)
    n_max = max(result["n"] for result in results)
    conjecture_holds = all(result["g_ent"] >= result["rank"] for result in results)
    counterexample = "" if conjecture_holds else f"n={results[0]['n']}, g_ent={results[0]['g_ent']}, rank={results[0]['rank']}"
    
    return {
        "metric_name": "geometric_entropy",
        "metric_value": sum(result["g_ent"] for result in results) / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['n']}, g_ent={results[0]['g_ent']}, rank={results[0]['rank']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")