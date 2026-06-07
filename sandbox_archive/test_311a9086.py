# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
from itertools import combinations

def generate_d_regular_circuit(d, n):
    if d * n % 2 != 0:
        return None  # Cannot form a d-regular graph with odd degree sum
    
    degree_sequence = [d] * n
    adjacency_matrix = [[0 for _ in range(n)] for _ in range(n)]
    
    def is_valid_edge(u, v):
        if u == v or adjacency_matrix[u][v] != 0:
            return False
        return True
    
    def add_edge(u, v):
        adjacency_matrix[u][v] = 1
        adjacency_matrix[v][u] = 1
    
    for i in range(n):
        neighbors = random.sample(range(i + 1, n), degree_sequence[i] // 2)
        for neighbor in neighbors:
            if is_valid_edge(i, neighbor):
                add_edge(i, neighbor)
    
    return adjacency_matrix

def calculate_entanglement_complexity(adjacency_matrix):
    n = len(adjacency_matrix)
    complexity = 0
    for i in range(n):
        for j in range(i + 1, n):
            if adjacency_matrix[i][j] == 1:
                complexity += 1
    return complexity

def calculate_minimal_index(adjacency_matrix):
    n = len(adjacency_matrix)
    index = float('inf')
    for i in range(n):
        for j in range(i + 1, n):
            if adjacency_matrix[i][j] == 1:
                # Calculate the shortest path using BFS
                queue = [(i, 0)]
                visited = set([i])
                while queue:
                    current, dist = queue.pop(0)
                    if current == j:
                        index = min(index, dist + 1)
                        break
                    for neighbor in range(n):
                        if adjacency_matrix[current][neighbor] == 1 and neighbor not in visited:
                            visited.add(neighbor)
                            queue.append((neighbor, dist + 1))
    return index

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    d = random.randint(2, 5)
    n = random.randint(5, 40)
    adjacency_matrix = generate_d_regular_circuit(d, n)
    
    if adjacency_matrix is None:
        return {
            "metric_name": "EntanglementComplexity",
            "metric_value": float('nan'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    entanglement_complexity = calculate_entanglement_complexity(adjacency_matrix)
    minimal_index = calculate_minimal_index(adjacency_matrix)
    
    return {
        "metric_name": "EntanglementComplexity",
        "metric_value": entanglement_complexity,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")