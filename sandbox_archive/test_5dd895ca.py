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
    
    def generate_quiver(n, m):
        vertices = list(range(n))
        edges = []
        for _ in range(m):
            u = random.choice(vertices)
            v = random.choice(vertices)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                edges.append((u, v))
        return vertices, edges
    
    def compute_minimal_order_of_automorphisms(vertices, edges):
        n = len(vertices)
        adj_matrix = [[0] * n for _ in range(n)]
        for u, v in edges:
            adj_matrix[u][v] = 1
            adj_matrix[v][u] = 1
        
        def gaussian_elimination(matrix):
            m, n = len(matrix), len(matrix[0])
            rank = 0
            for i in range(m):
                if rank < n:
                    pivot_row = i + [j for j in range(i, m) if matrix[j][i] != 0]
                    if not pivot_row:
                        continue
                    pivot_row_idx = pivot_row.index(max(pivot_row, key=abs))
                    matrix[i], matrix[pivot_row_idx] = matrix[pivot_row_idx], matrix[i]
                    for j in range(n):
                        if i != j:
                            factor = -matrix[j][i] / matrix[i][i]
                            for k in range(n):
                                matrix[j][k] += factor * matrix[i][k]
                    rank += 1
            return rank
        
        return n - gaussian_elimination(adj_matrix)
    
    def generate_arithmetic_circuit(m):
        # Simplified circuit generation for demonstration purposes
        return random.randint(1, m)
    
    def compute_communication_complexity(circuit, m):
        # Simplified communication complexity calculation
        return math.sqrt(m) * circuit
    
    n = 40
    m = random.randint(1, n * (n - 1) // 2)
    vertices, edges = generate_quiver(n, m)
    minimal_order = compute_minimal_order_of_automorphisms(vertices, edges)
    circuit = generate_arithmetic_circuit(m)
    communication_complexity = compute_communication_complexity(circuit, m)
    
    if minimal_order <= 0 or communication_complexity <= 0:
        return {
            "metric_name": "communication_complexity",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    if abs(communication_complexity - math.sqrt(m)) > 1:
        return {
            "metric_name": "communication_complexity",
            "metric_value": communication_complexity,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"Communication complexity {communication_complexity} is not within 1 of sqrt({m})"
        }
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": communication_complexity,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results if res["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results if res["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"communication complexity out of bounds\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")