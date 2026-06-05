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
    
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    def generate_d_regular_graph(d: int, n: int) -> list:
        if d * n % 2 != 0 or n < 2 * d:
            raise ValueError("Graph size must be a multiple of the degree")
        
        graph = [[] for _ in range(n)]
        edges = set()
        
        def add_edge(u, v):
            if (u, v) not in edges and (v, u) not in edges:
                graph[u].append(v)
                graph[v].append(u)
                edges.add((u, v))
                edges.add((v, u))
        
        for i in range(n):
            for j in range(i + 1, n):
                if len(graph[i]) < d and len(graph[j]) < d:
                    add_edge(i, j)
    
    def automorphism_group_size(graph: list) -> int:
        n = len(graph)
        visited = [False] * n
        group_size = 0
        
        def dfs(node, perm):
            if visited[node]:
                return True
            visited[node] = True
            for neighbor in graph[node]:
                if not visited[neighbor]:
                    if perm[neighbor] != perm[node]:
                        return False
                    if not dfs(neighbor, perm):
                        return False
            return True
        
        def generate_permutations():
            nonlocal group_size
            n = len(graph)
            elements = list(range(n))
            
            def backtrack(start):
                if start == n:
                    if all(dfs(i, {i: elements[i] for i in range(n)}) for i in range(n)):
                        group_size += 1
                    return
                for i in range(start, n):
                    elements[start], elements[i] = elements[i], elements[start]
                    backtrack(start + 1)
                    elements[start], elements[i] = elements[i], elements[start]
            
            backtrack(0)
        
        generate_permutations()
        return group_size
    
    def frege_proof_tree_width(graph: list) -> int:
        n = len(graph)
        visited = [False] * n
        max_width = 0
        
        def dfs(node, level):
            nonlocal max_width
            if visited[node]:
                return level - 1
            visited[node] = True
            width = 0
            for neighbor in graph[node]:
                width = max(width, dfs(neighbor, level + 1))
            max_width = max(max_width, width)
            return width
        
        for i in range(n):
            if not visited[i]:
                dfs(i, 0)
        
        return max_width
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        d = random.randint(2, min(n - 1, 6))
        graph = generate_d_regular_graph(d, n)
        
        group_size = automorphism_group_size(graph)
        proof_tree_width = frege_proof_tree_width(graph)
        
        if group_size == 0 or proof_tree_width == 0:
            continue
        
        log2_group_size = math.log2(group_size)
        results.append((log2_group_size, proof_tree_width))
    
    if not results:
        return {
            "metric_name": "log2(|A(G)|) vs w_Frege(G)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "graph_generation_failed"
        }
    
    mean_log2_group_size = sum(x for x, _ in results) / len(results)
    mean_proof_tree_width = sum(y for _, y in results) / len(results)
    correlation_coefficient = 0
    
    if len(results) > 1:
        numerator = sum((x - mean_log2_group_size) * (y - mean_proof_tree_width) for x, y in results)
        denominator = math.sqrt(sum((x - mean_log2_group_size) ** 2 for x, _ in results)) * math.sqrt(sum((y - mean_proof_tree_width) ** 2 for _, y in results))
        correlation_coefficient = numerator / denominator
    
    mean_abs_diff = sum(abs(x - y) for x, y in results) / len(results)
    
    return {
        "metric_name": "log2(|A(G)|) vs w_Frege(G)",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8 and mean_abs_diff <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = len([result for result in results if result["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_supported\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")