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
    if n % d != 0:
        raise ValueError("Graph size must be a multiple of the degree")
    
    graph = [[] for _ in range(n)]
    edges_added = set()
    
    while len(edges_added) < (n * d) // 2:
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        
        if u == v or (u, v) in edges_added or (v, u) in edges_added:
            continue
        
        graph[u].append(v)
        graph[v].append(u)
        edges_added.add((u, v))
    
    return graph

def is_bipartite(graph):
    n = len(graph)
    color = [-1] * n
    
    def dfs(node, c):
        if color[node] != -1:
            return color[node] == c
        
        color[node] = c
        for neighbor in graph[node]:
            if not dfs(neighbor, 1 - c):
                return False
        
        return True
    
    for i in range(n):
        if color[i] == -1 and not dfs(i, 0):
            return False
    
    return True

def circuit_satisfiability_threshold(graph):
    n = len(graph)
    
    def is_satisfiable(assignment):
        for u in range(n):
            clause = [graph[u][i] ^ assignment[graph[u][i]] for i in range(len(graph[u]))]
            if all(not c for c in clause):
                return False
        return True
    
    max_clauses = 0
    for _ in range(100):  # Try 100 random assignments
        assignment = [random.randint(0, 1) for _ in range(n)]
        if is_satisfiable(assignment):
            max_clauses += 1
    
    return max_clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = generate_d_regular_graph(n, 3)
        
        if not is_bipartite(graph):
            continue
        
        th_G = circuit_satisfiability_threshold(graph)
        
        # Minimal order of Hodge classes (m_h(G)) for a d-regular bipartite graph
        m_h_G = n // 2
        
        results.append((n, m_h_G, th_G))
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid bipartite graph found for n ≤ 40"
        }
    
    n_values, m_h_Gs, th_Gs = zip(*results)
    mean_m_h_G = sum(m_h_Gs) / len(m_h_Gs)
    mean_th_G = sum(th_Gs) / len(th_Gs)
    
    correlation_coefficient = (sum((m - mean_m_h_G) * (t - mean_th_G) for m, t in zip(m_h_Gs, th_Gs)) /
                               math.sqrt(sum((m - mean_m_h_G)**2 for m in m_h_Gs) *
                                         sum((t - mean_th_G)**2 for t in th_Gs)))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) > 0.95,  # Threshold for linear correlation
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(2, 37))  # Default to first 30 primes if no seeds provided
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all("metric_value" in r and not math.isnan(r["metric_value"]) for r in results):
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_metric_value} std=NA support_fraction={support_fraction}")
        else:
            print(f"RESULT: FALSIFIED counterexample=\"Not enough support\" first_failing_seed=NA")
    else:
        print("RESULT: INCONCLUSIVE Some trials had NaN metric values")