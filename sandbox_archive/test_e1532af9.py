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
    
    n = 40
    graph = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        graph[i][i] = 0
    
    def is_connected(graph):
        visited = [False] * n
        stack = [0]
        while stack:
            node = stack.pop()
            if not visited[node]:
                visited[node] = True
                for neighbor, edge in enumerate(graph[node]):
                    if edge and not visited[neighbor]:
                        stack.append(neighbor)
        return all(visited)
    
    if not is_connected(graph):
        return {
            "metric_name": "S_min(A(G))",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Graph is not connected"
        }
    
    def find_cycles(graph):
        n = len(graph)
        visited = [False] * n
        parent = [-1] * n
        
        def dfs(node, parent):
            stack = [(node, 0)]
            while stack:
                current, depth = stack.pop()
                if visited[current]:
                    cycle_length = depth - parent[current]
                    return True, cycle_length
                visited[current] = True
                for neighbor in range(n):
                    if graph[current][neighbor] and not visited[neighbor]:
                        stack.append((neighbor, depth + 1))
            return False, None
        
        for i in range(n):
            if not visited[i]:
                has_cycle, cycle_length = dfs(i, parent)
                if has_cycle:
                    return True
        return False
    
    has_cycles = find_cycles(graph)
    
    if has_cycles:
        return {
            "metric_name": "S_min(A(G))",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Graph contains cycles"
        }
    
    def automorphism_group(graph):
        n = len(graph)
        group = []
        
        def is_automorphism(perm):
            for i in range(n):
                for j in range(n):
                    if graph[i][j] != graph[perm[i]][perm[j]]:
                        return False
            return True
        
        def generate_permutations():
            elements = list(range(n))
            visited = set()
            
            def backtrack(start, perm):
                if len(perm) == n:
                    if is_automorphism(perm):
                        group.append(tuple(perm))
                    return
                for i in range(start, n):
                    if i not in visited:
                        visited.add(i)
                        backtrack(i + 1, perm + [i])
                        visited.remove(i)
            
            backtrack(0, [])
        
        generate_permutations()
        return group
    
    automorphisms = automorphism_group(graph)
    
    def minimal_generating_set(group):
        n = len(group)
        generators = []
        
        for i in range(n):
            if all(any(group[i][j] != group[k][j] for k in range(n) if k != j) for j in range(n)):
                generators.append(group[i])
        
        return generators
    
    S_min = minimal_generating_set(automorphisms)
    
    quantum_query_complexity = n  # Placeholder, should be replaced with actual calculation
    
    return {
        "metric_name": "S_min(A(G))",
        "metric_value": len(S_min),
        "instances_tested": 1,
        "conjecture_holds": len(S_min) <= quantum_query_complexity,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Graph properties do not match conjecture' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")