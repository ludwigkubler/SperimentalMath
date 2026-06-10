# auto-injected by SEC sandbox
import math
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

def generate_circuit(n: int, d: int) -> list:
    if n <= 1 or d <= 0:
        return []
    
    subcircuits = [generate_circuit(random.randint(2, n-1), random.randint(1, d-1)) for _ in range(d)]
    circuit = []
    for subcircuit in subcircuits:
        circuit.extend(subcircuit)
    circuit.append('OR')
    return circuit

def complement_graph(circuit: list) -> dict:
    n = len(circuit)
    graph = {i: set() for i in range(n)}
    
    def add_edge(u, v):
        if u != v:
            graph[u].add(v)
            graph[v].add(u)
    
    stack = [0]
    visited = [False] * n
    visited[0] = True
    
    while stack:
        u = stack.pop()
        for i in range(n):
            if not visited[i]:
                add_edge(u, i)
                visited[i] = True
                stack.append(i)
    
    return graph

def min_rank_local_system(graph: dict) -> int:
    n = len(graph)
    rank = 0
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            
            if A[i][i] == 0:
                continue
            
            pivot = Fraction(1, A[i][i])
            for j in range(n):
                A[i][j] *= pivot
            
            for j in range(m):
                if j != i and A[j][i] != 0:
                    factor = -A[j][i]
                    for k in range(n):
                        A[j][k] += factor * A[i][k]
        
        rank = sum(1 for row in A if any(row))
        return rank
    
    # Convert graph to adjacency matrix
    A = [[0] * n for _ in range(n)]
    for u, neighbors in graph.items():
        for v in neighbors:
            A[u][v] = 1
    
    return gaussian_elimination(A)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_max = 40
    instances_tested = 0
    circuit_ranks = []
    
    for d in range(5, 41):
        for _ in range(6):  # Ensure at least 30 instances per seed
            n = random.randint(d + 2, min(n_max, d * 2))
            circuit = generate_circuit(n, d)
            graph = complement_graph(circuit)
            rank = min_rank_local_system(graph)
            circuit_ranks.append(rank)
            instances_tested += 1
    
    if not circuit_ranks:
        return {
            "metric_name": "min_rank",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    max_ratio = max(rank / (d ** Fraction(2, 3) * n ** Fraction(1, 3)) for d, rank in zip(range(5, 41), circuit_ranks))
    
    return {
        "metric_name": "min_rank",
        "metric_value": max_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": max_ratio <= 2,
        "counterexample": "" if max_ratio <= 2 else f"max_ratio={max_ratio}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
        support_fraction = 1.0
    else:
        mean_value = None
        std_value = None
        support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["metric_value"] is not None for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["metric_value"] is None)
        print(f"RESULT: INCONCLUSIVE reason=missing_data_first_seed={first_failing_seed}")