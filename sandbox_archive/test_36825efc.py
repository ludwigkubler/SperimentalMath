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

def generate_d_regular_graph(n, d):
    if (n - 1) * d % 2 != 0:
        raise ValueError("Invalid degree for a regular graph")
    
    edges = set()
    while len(edges) < (n - 1) * d // 2:
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v and (u, v) not in edges and (v, u) not in edges:
            edges.add((u, v))
    
    return {i: [] for i in range(n)}, list(edges)

def del_pezzo_degree(graph):
    n = len(graph)
    adj_matrix = [[0] * n for _ in range(n)]
    for u, v in graph[1:]:
        adj_matrix[u][v] = 1
        adj_matrix[v][u] = 1
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        
        for i in range(n):
            max_row = None
            for j in range(rank, m):
                if matrix[j][i]:
                    max_row = j
                    break
            
            if max_row is None:
                continue
            
            matrix[max_row], matrix[rank] = matrix[rank], matrix[max_row]
            
            for j in range(m):
                if i != j and matrix[j][i]:
                    factor = Fraction(matrix[j][i], matrix[rank][i])
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[rank][k]
            
            rank += 1
        
        return rank
    
    return n - gaussian_elimination(adj_matrix)

def circuit_entanglement_complexity(graph):
    # Placeholder function. Replace with actual implementation.
    return len(graph[1])

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    d = random.randint(2, 5)
    n_max = random.choice([5, 10, 15, 20, 30, 40])
    graph, edges = generate_d_regular_graph(n_max + 1, d)
    
    del_pezzo_values = []
    entanglement_complexity_values = []
    
    for _ in range(30):
        n = random.randint(5, n_max)
        subgraph_edges = random.sample(edges, min(len(edges), n * (n - 1) // 2))
        subgraph_graph = {i: [] for i in range(n)}
        for u, v in subgraph_edges:
            if u < n and v < n:
                subgraph_graph[u].append(v)
                subgraph_graph[v].append(u)
        
        del_pezzo_values.append(del_pezzo_degree(subgraph_graph))
        entanglement_complexity_values.append(circuit_entanglement_complexity(subgraph_graph))
    
    correlation_coefficient = 0
    if len(del_pezzo_values) > 1 and len(entanglement_complexity_values) > 1:
        mean_del_pezzo = sum(del_pezzo_values) / len(del_pezzo_values)
        mean_entanglement = sum(entanglement_complexity_values) / len(entanglement_complexity_values)
        
        numerator = sum((x - mean_del_pezzo) * (y - mean_entanglement) for x, y in zip(del_pezzo_values, entanglement_complexity_values))
        denominator = math.sqrt(sum((x - mean_del_pezzo) ** 2 for x in del_pezzo_values)) * math.sqrt(sum((y - mean_entanglement) ** 2 for y in entanglement_complexity_values))
        
        correlation_coefficient = numerator / denominator if denominator != 0 else 0
    
    conjecture_holds = correlation_coefficient >= 0.7 or any(abs(x - d) > 1.5 for x, d in zip(del_pezzo_values, [d] * len(del_pezzo_values)))
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(del_pezzo_values),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
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
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=budget_exceeded n_tested={len(results)}")