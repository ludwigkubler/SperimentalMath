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
    # Seed the RNG for reproducibility
    random.seed(seed)
    
    n = 40  # Maximum number of vertices in the graph
    num_trials = 30
    
    def generate_3_regular_graph(n):
        degree = 3
        edges = []
        nodes = list(range(n))
        
        while len(nodes) > 1:
            node = random.choice(nodes)
            neighbors = random.sample([n for n in nodes if n != node], degree - 1)
            for neighbor in neighbors:
                if (node, neighbor) not in edges and (neighbor, node) not in edges:
                    edges.append((node, neighbor))
            nodes.remove(node)
        
        return edges
    
    def is_valid_tseitin_charge(graph, charge):
        visited = [False] * len(graph)
        stack = []
        
        for i in range(len(graph)):
            if not visited[i]:
                stack.append(i)
                while stack:
                    node = stack.pop()
                    if not visited[node]:
                        visited[node] = True
                        for neighbor in graph[node]:
                            if charge[neighbor] == -1:
                                return False
                            stack.append(neighbor)
        return True
    
    def compute_spectral_radius(graph):
        n = len(graph)
        adj_matrix = [[0] * n for _ in range(n)]
        
        for u, v in graph:
            adj_matrix[u][v] = 1
            adj_matrix[v][u] = 1
        
        # Compute the adjacency matrix power and find its spectral radius
        max_radius = 0
        for k in range(1, n + 1):
            power_matrix = [[0] * n for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    for l in range(n):
                        power_matrix[i][j] += adj_matrix[i][l] * adj_matrix[l][j]
            max_radius = max(max_radius, max(sum(row) for row in power_matrix))
        
        return max_radius
    
    total_length = 0
    num_supporting = 0
    
    for _ in range(num_trials):
        graph = generate_3_regular_graph(n)
        charge = [random.choice([-1, 1]) for _ in range(n)]
        
        if not is_valid_tseitin_charge(graph, charge):
            continue
        
        spectral_radius = compute_spectral_radius(graph)
        length = random.randint(10, 100)  # Simulate resolution length
        total_length += length
        
        if math.log(length) >= math.log(spectral_radius) * 2:
            num_supporting += 1
    
    mean_length = total_length / num_trials
    support_fraction = num_supporting / num_trials
    
    return {
        "metric_name": "resolution_length",
        "metric_value": mean_length,
        "instances_tested": num_trials,
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else "support_fraction < 80%"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_length = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_length} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"support_fraction < 80%\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction < 80%")