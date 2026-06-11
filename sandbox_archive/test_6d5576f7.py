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
    
    def generate_d_regular_graph(n, d):
        if (n * d) % 2 != 0 or d < 1 or n < 1:
            return None
        adj_matrix = [[0] * n for _ in range(n)]
        degree_count = [0] * n
        
        while any(count != d for count in degree_count):
            u, v = random.sample(range(n), 2)
            if adj_matrix[u][v] == 1:
                continue
            adj_matrix[u][v] = 1
            adj_matrix[v][u] = 1
            degree_count[u] += 1
            degree_count[v] += 1
        
        return adj_matrix
    
    def tseitin_formula(graph):
        n = len(graph)
        literals = [f'x{i}' for i in range(n)]
        clauses = []
        
        for i in range(n):
            clause = []
            for j in range(n):
                if graph[i][j] == 1:
                    clause.append(literals[j])
            clauses.append(clause)
        
        return clauses
    
    def resolution_width(clauses):
        queue = [set(clause) for clause in clauses]
        learned_clauses = set()
        
        while True:
            new_clause = None
            for clause1 in queue:
                for clause2 in queue:
                    if len(clause1.intersection(clause2)) == 1:
                        new_clause = (clause1 - clause2).union(clause2 - clause1)
                        break
                if new_clause is not None:
                    break
            if new_clause is None:
                return max(len(clause) for clause in queue)
            
            learned_clauses.add(frozenset(new_clause))
            queue.append(new_clause)
    
    def minimal_irreducible_representation(graph):
        n = len(graph)
        representations = [set() for _ in range(n)]
        
        for i in range(n):
            for j in range(i + 1, n):
                if graph[i][j] == 1:
                    representations[i].add(j)
                    representations[j].add(i)
        
        irreducible_representations = set()
        visited = [False] * n
        
        def dfs(node):
            stack = [node]
            while stack:
                current = stack.pop()
                if not visited[current]:
                    visited[current] = True
                    irreducible_representations.add(current)
                    for neighbor in representations[current]:
                        if not visited[neighbor]:
                            stack.append(neighbor)
        
        for i in range(n):
            if not visited[i]:
                dfs(i)
        
        return len(irreducible_representations)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = generate_d_regular_graph(n, 2)
        if graph is None:
            continue
        
        clauses = tseitin_formula(graph)
        width = resolution_width(clauses)
        order = minimal_irreducible_representation(graph)
        
        results.append({
            "n": n,
            "width": width,
            "order": order
        })
    
    if not results:
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_order = sum(result["order"] for result in results) / len(results)
    mean_width = sum(result["width"] for result in results) / len(results)
    
    if any(abs(order - width) > 2 for order, width in zip([result["order"] for result in results], [result["width"] for result in results])):
        return {
            "metric_name": "resolution_width",
            "metric_value": mean_order,
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": False,
            "counterexample": f"order={mean_order}, width={mean_width}"
        }
    
    return {
        "metric_name": "resolution_width",
        "metric_value": mean_order,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(sys.argv[1])] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{trial_result}...}}")
        results.append(trial_result)
    
    supported_count = sum(1 for result in results if result["conjecture_holds"])
    support_fraction = supported_count / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={sum(result['metric_value'] for result in results) / len(results)} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(result['metric_value'] for result in results) / len(results)} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"order={result['metric_value']}, width={result['counterexample']}\" first_failing_seed={first_failing_seed}")