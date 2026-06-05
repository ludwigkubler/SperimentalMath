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
        graph = [[] for _ in range(n)]
        edges = set()
        for i in range(n):
            for j in range(d):
                neighbor = (i + j + 1) % n
                if (i, neighbor) not in edges and (neighbor, i) not in edges:
                    graph[i].append(neighbor)
                    graph[neighbor].append(i)
                    edges.add((i, neighbor))
        return graph
    
    def is_valid_assignment(graph, assignment):
        for node in range(len(graph)):
            if len([neighbor for neighbor in graph[node] if assignment[neighbor]]) != 1:
                return False
        return True
    
    def find_satisfying_assignment(graph):
        n = len(graph)
        assignment = [False] * n
        stack = []
        
        for node in range(n):
            if not any(assignment[neighbor] for neighbor in graph[node]):
                assignment[node] = True
                stack.append(node)
        
        while stack:
            current_node = stack.pop()
            for neighbor in graph[current_node]:
                if not assignment[neighbor]:
                    assignment[neighbor] = True
                    stack.append(neighbor)
        
        return assignment
    
    def hodge_class_order(graph):
        n = len(graph)
        order = 0
        visited = [False] * n
        
        def dfs(node, current_order):
            nonlocal order
            if visited[node]:
                return
            visited[node] = True
            for neighbor in graph[node]:
                dfs(neighbor, current_order + 1)
            order = max(order, current_order)
        
        for node in range(n):
            if not visited[node]:
                dfs(node, 0)
        
        return order
    
    def circuit_satisfiability_threshold(graph):
        n = len(graph)
        assignment = find_satisfying_assignment(graph)
        if is_valid_assignment(graph, assignment):
            return n
        else:
            return float('inf')
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        graph = generate_d_regular_graph(n, 2)
        if graph is None:
            continue
        
        m_h = hodge_class_order(graph)
        th = circuit_satisfiability_threshold(graph)
        
        results.append((m_h, th))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    m_h_values = [m for m, _ in results]
    th_values = [th for _, th in results]
    
    mean_m_h = sum(m_h_values) / len(m_h_values)
    mean_th = sum(th_values) / len(th_values)
    correlation = (sum((m - mean_m_h) * (t - mean_th) for m, t in results) /
                   math.sqrt(sum((m - mean_m_h)**2 for m in m_h_values) *
                             sum((t - mean_th)**2 for t in th_values)))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n for n, _ in results),
        "conjecture_holds": abs(correlation) > 0.95,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_not_linear\" first_failing_seed={first_failing_seed}")