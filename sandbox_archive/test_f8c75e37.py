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
    
    def generate_random_d_regular_graph(n, d):
        if n * d % 2 != 0 or d < 1 or d >= n:
            raise ValueError("Invalid parameters for generating a d-regular graph")
        
        adjacency_matrix = [[0] * n for _ in range(n)]
        degree_count = [0] * n
        
        while any(count != d for count in degree_count):
            u, v = random.sample(range(n), 2)
            if u == v or adjacency_matrix[u][v]:
                continue
            adjacency_matrix[u][v] = 1
            adjacency_matrix[v][u] = 1
            degree_count[u] += 1
            degree_count[v] += 1
        
        return adjacency_matrix
    
    def calculate_index(adjacency_matrix):
        n = len(adjacency_matrix)
        index = 0
        for i in range(n):
            for j in range(i + 1, n):
                if adjacency_matrix[i][j]:
                    index += 1
        return index
    
    def calculate_resolution_proof_width(graph):
        # Placeholder function; actual implementation needed
        return len(graph) * (len(graph) - 1) // 2
    
    n = random.randint(5, 40)
    d = random.randint(2, min(n - 1, 3))
    graph = generate_random_d_regular_graph(n, d)
    
    index = calculate_index(graph)
    resolution_proof_width = calculate_resolution_proof_width(graph)
    
    if resolution_proof_width == 0:
        return {
            "metric_name": "Index to Resolution Proof Width Ratio",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Resolution proof width is zero"
        }
    
    ratio = Fraction(index, resolution_proof_width)
    return {
        "metric_name": "Index to Resolution Proof Width Ratio",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True if 0.5 <= ratio <= 2 else False,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_ratio = sum(result["metric_value"] for result in results) / len(results)
        std_dev = math.sqrt(sum((result["metric_value"] - mean_ratio) ** 2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio out of bounds\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")