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
from math import gcd, lcm
from fractions import Fraction

def generate_d_regular_graph(n, d):
    if n * d % 2 != 0:
        return None  # Cannot form a regular graph with odd degree sum
    
    graph = [[] for _ in range(n)]
    
    def add_edge(v1, v2):
        if v2 not in graph[v1]:
            graph[v1].append(v2)
            graph[v2].append(v1)
    
    for v in range(n):
        remaining_degrees = d - len(graph[v])
        available_neighbors = [u for u in range(n) if u != v and u not in graph[v]]
        
        if remaining_degrees > len(available_neighbors):
            return None  # Not enough neighbors to satisfy degree requirement
        
        neighbors_to_add = random.sample(available_neighbors, remaining_degrees)
        for neighbor in neighbors_to_add:
            add_edge(v, neighbor)
    
    return graph

def generate_random_d_regular_graphs(n, d, num_graphs=1):
    graphs = []
    while len(graphs) < num_graphs:
        graph = generate_d_regular_graph(n, d)
        if graph is not None:
            graphs.append(graph)
    return graphs

def compute_min_order(graph):
    orders = [len(set(graph[v])) for v in range(len(graph))]
    return lcm(*orders)

def tseitin_formula(n):
    clauses = []
    for i in range(1, n + 1):
        clauses.append([i])
        for j in range(i + 1, n + 1):
            clauses.append([-i, -j, i + j])
    return clauses

def resolution_width(clauses):
    queue = set()
    extended_queue = set()
    seen = set()
    
    def add_clause(c):
        if c not in queue:
            queue.add(c)
    
    for clause in clauses:
        add_clause(tuple(sorted(clause)))
    
    while queue:
        clause = min(queue, key=len)
        queue.remove(clause)
        
        if len(clause) == 1:
            return abs(clause[0])
        
        literal = clause[0]
        neg_literal = -literal
        
        for other_clause in clauses:
            if neg_literal in other_clause:
                new_clause = tuple(sorted([l for l in other_clause if l != neg_literal] + [l for l in clause if l != literal]))
                if new_clause not in seen:
                    seen.add(new_clause)
                    extended_queue.add(new_clause)
        
        queue.update(extended_queue)
        extended_queue.clear()
    
    return float('inf')

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 30
    d = 4
    
    graphs = generate_random_d_regular_graphs(n, d)
    if not graphs:
        return {
            "metric_name": "min_order(G)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "unable_to_generate_d_regular_graph"
        }
    
    min_orders = [compute_min_order(graph) for graph in graphs]
    widths = [resolution_width(tseitin_formula(n)) for _ in range(len(graphs))]
    
    if not all(widths):
        return {
            "metric_name": "min_order(G)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "resolution_width_not_computed"
        }
    
    correlation = sum((x - mean_min_orders) * (y - mean_widths) for x, y in zip(min_orders, widths)) / len(min_orders)
    p_value = 2 * (1 - abs(correlation) ** 0.5)  # Approximate p-value using Fisher's z-transform
    
    return {
        "metric_name": "min_order(G)",
        "metric_value": correlation,
        "instances_tested": len(graphs),
        "n_max": n,
        "conjecture_holds": correlation >= 0.5 and p_value <= 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3**j + 5**k for i in range(4) for j in range(4) for k in range(4)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.2f} std={std_metric_value:.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["metric_value"] is not None for r in results):
        print(f"RESULT: FALSIFIED counterexample=\"correlation_not_significant\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")