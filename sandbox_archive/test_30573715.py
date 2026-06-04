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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def nearest_neighbor_graph(boolean_function, n):
        graph = []
        for i in range(len(boolean_function)):
            distances = []
            for j in range(i + 1, len(boolean_function)):
                dist = sum(abs(a - b) for a, b in zip(bin(i)[2:].zfill(n), bin(j)[2:].zfill(n)))
                distances.append((j, dist))
            graph.append(distances)
        return graph
    
    def geometric_entropy(graph):
        n = len(graph)
        total_dist = 0
        count = 0
        for i in range(n):
            for j, dist in graph[i]:
                if dist == 1:
                    total_dist += 1
                    count += 1
        if count == 0:
            return 0
        avg_dist = total_dist / count
        entropy = -avg_dist * math.log2(avg_dist) - (1 - avg_dist) * math.log2(1 - avg_dist)
        return entropy
    
    def communication_complexity_matrix(graph):
        n = len(graph)
        matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j, dist in graph[i]:
                if dist == 1:
                    matrix[i][j] = 1
                    matrix[j][i] = 1
        return matrix
    
    def rank(matrix):
        n = len(matrix)
        augmented_matrix = [row + [0] for row in matrix]
        for i in range(n):
            max_row = max(range(i, n), key=lambda x: abs(augmented_matrix[x][i]))
            augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
            if augmented_matrix[i][i] == 0:
                continue
            for j in range(n + 1):
                augmented_matrix[i][j] /= augmented_matrix[i][i]
            for k in range(n):
                if k != i and augmented_matrix[k][i] != 0:
                    factor = augmented_matrix[k][i]
                    for j in range(n + 1):
                        augmented_matrix[k][j] -= factor * augmented_matrix[i][j]
        rank = sum(1 for row in augmented_matrix if any(row[j] != 0 for j in range(n)))
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        boolean_function = generate_random_boolean_function(n)
        graph = nearest_neighbor_graph(boolean_function, n)
        g_ent = geometric_entropy(graph)
        comm_matrix = communication_complexity_matrix(graph)
        rnk = rank(comm_matrix)
        
        if rnk == 0:
            continue
        
        results.append({
            "n": n,
            "g_ent": g_ent,
            "rnk": rnk
        })
    
    if not results:
        return {
            "metric_name": "geometric_entropy",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_valid_instances"
        }
    
    instances_tested = len(results)
    n_max = max(result["n"] for result in results)
    g_ent_values = [result["g_ent"] for result in results]
    rnk_values = [result["rnk"] for result in results]
    
    mean_g_ent = sum(g_ent_values) / instances_tested
    std_g_ent = math.sqrt(sum((x - mean_g_ent)**2 for x in g_ent_values) / instances_tested)
    
    conjecture_holds = all(g >= r for g, r in zip(g_ent_values, rnk_values))
    counterexample = "" if conjecture_holds else "g < r"
    
    return {
        "metric_name": "geometric_entropy",
        "metric_value": mean_g_ent,
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
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_g_ent = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_g_ent = math.sqrt(sum((r["metric_value"] - mean_g_ent)**2 for r in results if r["metric_value"] is not None) / len(results))
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_g_ent} std={std_g_ent} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")