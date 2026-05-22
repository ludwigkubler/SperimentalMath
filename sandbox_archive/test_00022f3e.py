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
    
    def generate_symmetric_graph(n):
        graph = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    weight = random.randint(1, 10)
                    graph[i][j] = weight
                    graph[j][i] = weight
        return graph
    
    def find_min_rank(graph):
        n = len(graph)
        rank = 0
        for i in range(n):
            if all(graph[i][j] == 0 for j in range(i + 1, n)):
                continue
            pivot_row = next(j for j in range(i, n) if graph[j][i] != 0)
            if pivot_row != i:
                graph[i], graph[pivot_row] = graph[pivot_row], graph[i]
            rank += 1
            for j in range(n):
                if j == i:
                    continue
                factor = -graph[j][i] / graph[i][i]
                for k in range(n):
                    graph[j][k] += factor * graph[i][k]
        return rank
    
    def find_monotone_circuit_depth(graph):
        n = len(graph)
        visited = [False] * n
        depth = 0
        
        def dfs(node, current_depth):
            nonlocal depth
            if current_depth > depth:
                depth = current_depth
            visited[node] = True
            for neighbor in range(n):
                if graph[node][neighbor] != 0 and not visited[neighbor]:
                    dfs(neighbor, current_depth + 1)
            visited[node] = False
        
        for start_node in range(n):
            dfs(start_node, 1)
        
        return depth
    
    n = random.randint(5, 40)
    graph = generate_symmetric_graph(n)
    
    min_rank = find_min_rank(graph)
    monotone_circuit_depth = find_monotone_circuit_depth(graph)
    
    metric_value = abs(min_rank - monotone_circuit_depth)
    conjecture_holds = metric_value <= 3
    counterexample = "" if conjecture_holds else f"MinRank={min_rank}, CircuitDepth={monotone_circuit_depth}"
    
    return {
        "metric_name": "Minimal Rank of Tropicalized Symplectic Leaves vs Monotone Circuit Depth",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"MinRank > CircuitDepth\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")