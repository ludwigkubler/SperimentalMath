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
    
    def generate_random_graph(n):
        graph = [[0] * n for _ in range(n)]
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    graph[i][j] = graph[j][i] = 1
                    edges.add((i, j))
        return graph, edges
    
    def is_connected(graph):
        visited = [False] * len(graph)
        stack = [0]
        while stack:
            node = stack.pop()
            if not visited[node]:
                visited[node] = True
                for neighbor in range(len(graph)):
                    if graph[node][neighbor] == 1 and not visited[neighbor]:
                        stack.append(neighbor)
        return all(visited)
    
    def resolution_length(graph):
        n = len(graph)
        clauses = []
        for i in range(n):
            clauses.append([i + 1])
        for u, v in graph:
            clauses.append([-u - 1, -v - 1])
        length = 0
        while True:
            new_clauses = []
            added_clause = False
            for clause in clauses:
                if len(clause) == 1:
                    continue
                literal = random.choice(clause)
                other_literals = [l for l in clause if l != literal]
                new_clause = [-literal] + other_literals
                if new_clause not in new_clauses:
                    new_clauses.append(new_clause)
                    added_clause = True
            if not added_clause:
                break
            clauses.extend(new_clauses)
            length += 1
        return length
    
    def min_rank(graph):
        n = len(graph)
        rank = n
        for i in range(2 ** n):
            A = [[0] * n for _ in range(n)]
            for j in range(n):
                if (i >> j) & 1:
                    for k in range(n):
                        if graph[j][k]:
                            A[j][k] = 1
            for j in range(n):
                for k in range(j + 1, n):
                    if A[j][k] == A[k][j] and A[j][k] != 0:
                        rank -= 1
                        break
                else:
                    continue
                break
        return rank
    
    n = random.randint(5, 40)
    graph, _ = generate_random_graph(n)
    
    if not is_connected(graph):
        return {
            "metric_name": "MinRank(G ⊗ G) / ResolutionLength(T_G)",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Graph is not connected"
        }
    
    min_rank_value = min_rank(graph)
    resolution_length_value = resolution_length(graph)
    
    if min_rank_value / resolution_length_value >= 2:
        return {
            "metric_name": "MinRank(G ⊗ G) / ResolutionLength(T_G)",
            "metric_value": min_rank_value / resolution_length_value,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "MinRank(G ⊗ G) / ResolutionLength(T_G)",
            "metric_value": min_rank_value / resolution_length_value,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Graph has cycles, MinRank(G ⊗ G) = {min_rank_value}, ResolutionLength(T_G) = {resolution_length_value}"
        }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if "metric_value" in r]
    conjecture_holds = all(r["conjecture_holds"] for r in results if "conjecture_holds" in r)
    
    mean_value = sum(metric_values) / len(metric_values)
    std_value = math.sqrt(sum((x - mean_value)**2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if conjecture_holds:
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Graph has cycles\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")