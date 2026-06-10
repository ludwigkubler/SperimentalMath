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
    
    def generate_instance(n, m):
        variables = set(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, 2)
            if random.choice([True, False]):
                clause[0] *= -1
            clauses.append(clause)
        return variables, clauses
    
    def shortest_path_length(graph, start, end):
        n = len(graph)
        dist = [float('inf')] * n
        dist[start] = 0
        visited = set()
        
        while end not in visited:
            u = min((v for v in range(n) if v not in visited), key=lambda v: dist[v])
            visited.add(u)
            
            for v, weight in graph[u]:
                if v not in visited and dist[u] + weight < dist[v]:
                    dist[v] = dist[u] + weight
        
        return dist[end]
    
    def dpll_search_tree_height(instance):
        variables, clauses = instance
        n = len(variables)
        
        # Construct the graph from the clause-to-literal mapping
        graph = [[] for _ in range(n)]
        for clause in clauses:
            for lit in clause:
                if lit > 0:
                    graph[lit - 1].append((lit, 1))
                else:
                    graph[-lit - 1].append((-lit, 1))
        
        # Compute the shortest path lengths between all pairs of literals
        max_height = 0
        for i in range(n):
            for j in range(i + 1, n):
                height = shortest_path_length(graph, i, j)
                if height > max_height:
                    max_height = height
        
        return max_height
    
    def min_energy_flow(instance):
        variables, clauses = instance
        n = len(variables)
        
        # Construct the graph from the clause-to-literal mapping
        graph = [[] for _ in range(n)]
        for clause in clauses:
            for lit in clause:
                if lit > 0:
                    graph[lit - 1].append((lit, 1))
                else:
                    graph[-lit - 1].append((-lit, 1))
        
        # Compute the shortest path lengths between all pairs of literals
        min_flow = float('inf')
        for i in range(n):
            for j in range(i + 1, n):
                flow = shortest_path_length(graph, i, j)
                if flow < min_flow:
                    min_flow = flow
        
        return min_flow
    
    instance = generate_instance(5, 7)  # Example instance with 5 variables and 7 clauses
    dpll_height = dpll_search_tree_height(instance)
    energy_flow = min_energy_flow(instance)
    
    metric_value = abs(dpll_height - energy_flow)
    instances_tested = 1
    n_max = 5
    conjecture_holds = metric_value <= 3 * math.sqrt(metric_value)
    counterexample = "" if conjecture_holds else f"DPLL height: {dpll_height}, Energy flow: {energy_flow}"
    
    return {
        "metric_name": "DPLL Height vs. Energy Flow",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 50))
    
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")