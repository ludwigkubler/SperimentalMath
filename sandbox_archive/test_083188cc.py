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
from fractions import Fraction
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.add((i, j))
        return {i: [] for i in range(n)}, edges
    
    def add_edges(graph, edges):
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)
    
    def matrix_rank(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if all(matrix[j][i] == 0 for j in range(rank)):
                continue
            rank += 1
            factor = matrix[i][i]
            for j in range(i, n):
                matrix[i][j] /= factor
            for k in range(n):
                if k != i:
                    factor = matrix[k][i]
                    for j in range(i, n):
                        matrix[k][j] -= factor * matrix[i][j]
        return rank
    
    def communication_complexity_rank_variance(graph, inputs):
        n = len(graph)
        m = len(inputs[0])
        rank_variances = [0] * m
        for i in range(m):
            freqs = [0] * n
            for u in graph:
                for v in graph[u]:
                    if inputs[v][i] != inputs[u][i]:
                        freqs[v] += 1
            rank_variances[i] = sum(freq / (n - 1) for freq in freqs)
        return sum(rank_variances) / m
    
    def generate_inputs(n, m):
        inputs = []
        for _ in range(m):
            input_ = [random.choice([0, 1]) for _ in range(n)]
            inputs.append(input_)
        return inputs
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    total_variance = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        graph, edges = generate_graph(n)
        add_edges(graph, edges)
        inputs = generate_inputs(n, 2)
        
        rank_A = matrix_rank(graph)
        variance = communication_complexity_rank_variance(graph, inputs)
        
        total_rank += rank_A
        total_variance += variance
        instances_tested += len(inputs) * len(inputs[0])
        n_max = max(n_max, n)
    
    mean_rank = Fraction(total_rank, instances_tested)
    mean_variance = Fraction(total_variance, instances_tested)
    
    conjecture_holds = all(mean_rank <= mean_variance for _ in range(10))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Rank Variance",
        "metric_value": float(mean_variance),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")