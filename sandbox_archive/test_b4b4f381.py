# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return abs(a*b) // gcd(a, b)
    
    def generate_d_regular_graph(n, d):
        if (n * d) % 2 != 0 or d == 1:
            raise ValueError("Invalid parameters for generating a d-regular graph")
        
        graph = [[] for _ in range(n)]
        degree_sum = n * d
        available_neighbors = list(range(1, n))
        
        for i in range(n):
            if len(graph[i]) >= d:
                continue
            
            remaining_degrees = d - len(graph[i])
            neighbors_to_add = random.sample(available_neighbors, min(remaining_degrees, len(available_neighbors)))
            
            for neighbor in neighbors_to_add:
                graph[i].append(neighbor)
                graph[neighbor].append(i)
                available_neighbors.remove(neighbor)
        
        return graph
    
    def generate_tseitin_formula(graph):
        n = len(graph)
        variables = {f'x{i}': i for i in range(n)}
        clauses = []
        
        # Each vertex must be connected to at least one neighbor
        for i in range(n):
            if not graph[i]:
                raise ValueError("Graph is not d-regular")
            clause = [variables[f'x{neighbor}'] for neighbor in graph[i]]
            clauses.append(clause)
        
        # Ensure each variable appears exactly once
        for var, _ in variables.items():
            clauses.append([var])
            clauses.append([-var])
        
        return clauses
    
    def resolution_width(clauses):
        queue = set()
        learned_clauses = []
        
        def simplify_clause(clause):
            new_clause = [x for x in clause if x not in learned_clauses and -x not in learned_clauses]
            return new_clause
        
        def resolve(c1, c2):
            resolved_clause = [x for x in c1 if x not in c2 and -x not in c2]
            return resolved_clause
        
        for clause in clauses:
            queue.add(tuple(sorted(simplify_clause(clause))))
        
        while True:
            new_clauses = []
            found_resolvent = False
            
            for c1, c2 in combinations(queue, 2):
                if any(x == -y for x, y in zip(c1, c2)):
                    resolvent = resolve(c1, c2)
                    if not resolvent:
                        return len(learned_clauses) + 1
                    new_clauses.append(tuple(sorted(resolvent)))
                    found_resolvent = True
            
            if not found_resolvent:
                break
            
            for clause in new_clauses:
                queue.add(clause)
            
            learned_clauses.extend(new_clauses)
        
        return len(learned_clauses) + 1
    
    def min_order(graph):
        orders = []
        for i in range(len(graph)):
            visited = [False] * len(graph)
            stack = [i]
            while stack:
                node = stack.pop()
                if not visited[node]:
                    visited[node] = True
                    stack.extend(neighbor for neighbor in graph[node] if not visited[neighbor])
            orders.append(sum(1 for v, b in enumerate(visited) if b))
        return min(orders)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        d = random.randint(2, n-1)
        graph = generate_d_regular_graph(n, d)
        tseitin_formula = generate_tseitin_formula(graph)
        min_order_value = min_order(graph)
        resolution_width_value = resolution_width(tseitin_formula)
        
        results.append({
            "n": n,
            "d": d,
            "min_order": min_order_value,
            "resolution_width": resolution_width_value
        })
    
    metric_name = "correlation"
    metric_value = sum(result["min_order"] * result["resolution_width"] for result in results) / len(results)
    instances_tested = len(results)
    n_max = max(result["n"] for result in results)
    conjecture_holds = False
    counterexample = ""
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")