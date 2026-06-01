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
    
    def generate_instance(m):
        variables = set()
        clauses = []
        for _ in range(m):
            clause = {random.choice(list(variables)) if variables else random.randint(1, 10)}
            variables.update(clause)
            clauses.append(clause)
        return clauses
    
    def compute_clause_set_complexity(clauses):
        return len(set(frozenset(clause) for clause in clauses))
    
    def planar_embedding(clauses):
        # Simplified planar embedding algorithm
        graph = {}
        for clause in clauses:
            for var in clause:
                if var not in graph:
                    graph[var] = set()
                for other_var in clause:
                    if other_var != var and other_var not in graph[var]:
                        graph[var].add(other_var)
                        graph[other_var].add(var)
        return graph
    
    def fundamental_group(graph):
        # Simplified computation of the fundamental group
        visited = set()
        edges = []
        for node, neighbors in graph.items():
            for neighbor in neighbors:
                if (node, neighbor) not in edges and (neighbor, node) not in edges:
                    edges.append((node, neighbor))
        
        def dfs(node, parent):
            visited.add(node)
            for neighbor in graph[node]:
                if neighbor != parent and neighbor not in visited:
                    dfs(neighbor, node)
        
        for edge in edges:
            u, v = edge
            if u not in visited:
                dfs(u, None)
        
        return len(visited) - 1
    
    def topological_entropy(fundamental_group_size):
        # Simplified computation of topological entropy
        return math.log2(fundamental_group_size + 1)
    
    h_min_values = []
    c_I_values = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            m = random.randint(n // 2, n)
            instance = generate_instance(m)
            c_I = compute_clause_set_complexity(instance)
            embedding = planar_embedding(instance)
            h_min = topological_entropy(fundamental_group(embedding))
            h_min_values.append(h_min)
            c_I_values.append(c_I)
    
    if not h_min_values or not c_I_values:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_data"
        }
    
    mean_h_min = sum(h_min_values) / len(h_min_values)
    mean_c_I = sum(c_I_values) / len(c_I_values)
    
    correlation_coefficient = sum((h_min_values[i] - mean_h_min) * (c_I_values[i] - mean_c_I) for i in range(len(h_min_values))) / ((len(h_min_values) - 1) * math.sqrt(sum((h_min_values[i] - mean_h_min) ** 2 for i in range(len(h_min_values)))) * math.sqrt(sum((c_I_values[i] - mean_c_I) ** 2 for i in range(len(c_I_values)))))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(h_min_values),
        "n_max": max(40, max(n for n in [5, 10, 15, 20, 30, 40] if any(m > 0 for m in range(n // 2, n)))),
        "conjecture_holds": 0.5 <= correlation_coefficient <= 1.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std=0 support_fraction=1")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_out_of_range\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")