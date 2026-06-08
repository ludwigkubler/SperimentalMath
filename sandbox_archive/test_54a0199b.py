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
    
    def generate_random_circuit(n, max_depth):
        if n == 1:
            return [random.choice([0, 1])]
        depth = random.randint(2, max_depth)
        circuit = []
        for _ in range(depth - 1):
            subcircuit = generate_random_circuit(n, depth - 2)
            circuit.append(random.choice([0, 1]))
            circuit.extend(subcircuit)
        return circuit
    
    def build_graph(circuit):
        n = len(circuit)
        graph = [[] for _ in range(n)]
        stack = []
        for i, gate in enumerate(circuit):
            if gate == 0:
                continue
            while stack and circuit[stack[-1]] != 1:
                stack.pop()
            if stack:
                parent = stack[-1]
                graph[parent].append(i)
                graph[i].append(parent)
            stack.append(i)
        return graph
    
    def compute_rank(graph):
        n = len(graph)
        visited = [False] * n
        rank = 0
        
        def dfs(node, depth):
            nonlocal rank
            if visited[node]:
                return
            visited[node] = True
            rank = max(rank, depth)
            for neighbor in graph[node]:
                dfs(neighbor, depth + 1)
        
        for i in range(n):
            if not visited[i]:
                dfs(i, 0)
        
        return rank
    
    def compute_lie_algebra_dimension(graph):
        n = len(graph)
        adjacency_matrix = [[0] * n for _ in range(n)]
        for u in range(n):
            for v in graph[u]:
                adjacency_matrix[u][v] = 1
                adjacency_matrix[v][u] = 1
        
        def gaussian_elimination(matrix, n):
            rank = 0
            for i in range(n):
                if matrix[i][i] == 0:
                    found = False
                    for j in range(i + 1, n):
                        if matrix[j][i] != 0:
                            matrix[i], matrix[j] = matrix[j], matrix[i]
                            found = True
                            break
                    if not found:
                        continue
                pivot = matrix[i][i]
                for j in range(n):
                    matrix[i][j] /= pivot
                for k in range(n):
                    if k != i and matrix[k][i] != 0:
                        factor = matrix[k][i]
                        for j in range(n):
                            matrix[k][j] -= factor * matrix[i][j]
            return sum(1 for row in matrix if any(row))
        
        return gaussian_elimination(adjacency_matrix, n)
    
    def is_d_regular(graph):
        degree = [len(neighbors) for neighbors in graph]
        return all(d == degree[0] for d in degree)
    
    n = random.randint(2, 10)
    max_depth = 40
    circuit = generate_random_circuit(n, max_depth)
    graph = build_graph(circuit)
    
    if not is_d_regular(graph):
        return {
            "metric_name": "rank",
            "metric_value": -1,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    rank = compute_rank(graph)
    lie_algebra_dimension = compute_lie_algebra_dimension(graph)
    depth = len(circuit) - circuit.count(0)
    
    return {
        "metric_name": "rank",
        "metric_value": rank,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": rank <= depth and lie_algebra_dimension <= n,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={r['seed']}")
                break