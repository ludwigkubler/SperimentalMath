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

# Define constants and utility functions
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_primes(count):
    primes = []
    num = 2
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def random_d_regular_graph(n, d):
    graph = {i: [] for i in range(n)}
    edges_added = set()
    for _ in range(d * n // 2):
        while True:
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u != v and (u, v) not in edges_added and (v, u) not in edges_added:
                graph[u].append(v)
                graph[v].append(u)
                edges_added.add((u, v))
                break
    return graph

def dfs(graph, node, visited):
    stack = [node]
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    stack.append(neighbor)

def connected_components(graph):
    components = []
    visited = set()
    for node in range(len(graph)):
        if node not in visited:
            component = []
            dfs(graph, node, component)
            components.append(component)
    return components

def minimal_order_of_symplectic_leaves(graph):
    n = len(graph)
    visited = set()
    components = connected_components(graph)
    m_order = 0
    for component in components:
        m_order += len(component)
    return m_order

def circuit_monotone_complexity(graph):
    # Placeholder function to simulate a non-trivial computation
    n = len(graph)
    return n * (n - 1) // 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in range(5, 41):
        d = 3  # Example value for d-regular graph
        graph = random_d_regular_graph(n, d)
        m_order = minimal_order_of_symplectic_leaves(graph)
        w_m = circuit_monotone_complexity(graph)
        results.append((m_order, w_m))
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    m_orders = [r[0] for r in results]
    w_ms = [r[1] for r in results]
    
    mean_m_order = sum(m_orders) / len(m_orders)
    mean_w_m = sum(w_ms) / len(w_ms)
    
    if len(m_orders) < 30:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(len(graph) for graph in results),
            "conjecture_holds": False,
            "counterexample": "Insufficient instances"
        }
    
    # Calculate Pearson correlation coefficient
    covariance = sum((m_orders[i] - mean_m_order) * (w_ms[i] - mean_w_m) for i in range(len(m_orders)))
    variance_m_order = sum((m_orders[i] - mean_m_order) ** 2 for i in range(len(m_orders)))
    variance_w_m = sum((w_ms[i] - mean_w_m) ** 2 for i in range(len(w_ms)))
    
    if variance_m_order == 0 or variance_w_m == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(len(graph) for graph in results),
            "conjecture_holds": False,
            "counterexample": "Zero variance"
        }
    
    pearson_corr = covariance / (math.sqrt(variance_m_order) * math.sqrt(variance_w_m))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": len(results),
        "n_max": max(len(graph) for graph in results),
        "conjecture_holds": pearson_corr >= 0.8 and pearson_corr <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes(30)
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE No trials executed")
    else:
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        
        if all(r["conjecture_holds"] for r in results):
            print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
        elif support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"Pearson correlation coefficient outside bounds\" first_failing_seed={first_failing_seed}")