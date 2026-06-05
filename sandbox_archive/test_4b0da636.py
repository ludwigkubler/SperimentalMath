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
        if n % d != 0:
            return None
        graph = {i: [] for i in range(n)}
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if len(graph[i]) < d and len(graph[j]) < d:
                    graph[i].append(j)
                    graph[j].append(i)
                    edges.add((i, j))
        return graph
    
    def compute_local_induction_dimension(graph):
        n = len(graph)
        visited = [False] * n
        stack = []
        
        def dfs(node):
            if visited[node]:
                return 0
            visited[node] = True
            stack.append(node)
            dim = 1
            for neighbor in graph[node]:
                dim = max(dim, dfs(neighbor))
            stack.pop()
            return dim
        
        for node in range(n):
            if not visited[node]:
                dim = dfs(node)
                if dim > n:
                    return None
        return n
    
    def compute_clause_subset_entropy(clauses):
        num_clauses = len(clauses)
        entropy = 0
        for clause in clauses:
            p = len(clause) / num_clauses
            entropy -= p * math.log2(p)
        return entropy
    
    def generate_sat_formula(graph, d):
        n = len(graph)
        variables = list(range(n))
        clauses = []
        
        def is_clause_valid(clause):
            for i in range(len(clause)):
                for j in range(i + 1, len(clause)):
                    if clause[i] == -clause[j]:
                        return False
            return True
        
        def backtrack(index):
            if index == n:
                return True
            for var in variables:
                clause = [var]
                if is_clause_valid(clause) and all(var not in graph[node] or -var not in clauses[graph[node].index(var)] for node in range(n)):
                    clauses.append(clause)
                    if backtrack(index + 1):
                        return True
                    clauses.pop()
            return False
        
        backtrack(0)
        return clauses
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = generate_d_regular_graph(n, 3)
        if graph is None:
            continue
        clauses = generate_sat_formula(graph, 3)
        if not clauses:
            continue
        
        ltd = compute_local_induction_dimension(graph)
        if ltd is None:
            continue
        
        entropy = compute_clause_subset_entropy(clauses)
        
        results.append({
            "n": n,
            "ltd": ltd,
            "entropy": entropy
        })
    
    if len(results) < 24:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results) if results else 0,
            "conjecture_holds": False,
            "counterexample": "insufficient_data"
        }
    
    correlation_sum = 0
    n_sum = 0
    for i in range(len(results)):
        for j in range(i + 1, len(results)):
            n_sum += results[i]["n"] * results[j]["n"]
            correlation_sum += (results[i]["ltd"] - results[j]["ltd"]) * (results[i]["entropy"] - results[j]["entropy"])
    
    n_mean = sum(result["n"] for result in results) / len(results)
    correlation_coefficient = correlation_sum / (len(results) * (len(results) - 1) * n_mean)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": correlation_coefficient >= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["metric_value"] is None for result in results):
        print("RESULT: INCONCLUSIVE insufficient_data")
    else:
        metric_values = [result["metric_value"] for result in results if result["metric_value"] is not None]
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={sum(metric_values) / len(metric_values)} std={math.sqrt(sum((x - sum(metric_values) / len(metric_values)) ** 2 for x in metric_values) / len(metric_values))} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient\" first_failing_seed={first_failing_seed}")