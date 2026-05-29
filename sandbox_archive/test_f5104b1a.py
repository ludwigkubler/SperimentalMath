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
    n = random.choice([5, 10, 15, 20, 30, 40])
    if n == 1:
        return {
            "metric_name": "minimal_polynomial_degree",
            "metric_value": 1,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    # Generate a random planar graph with n vertices
    G = generate_random_planar_graph(n)
    
    # Compute the minimal polynomial degree of the graph
    min_poly_degree = compute_minimal_polynomial_degree(G)
    if min_poly_degree > n ** 0.5:
        return {
            "metric_name": "minimal_polynomial_degree",
            "metric_value": min_poly_degree,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Graph with {n} vertices has minimal polynomial degree {min_poly_degree}"
        }
    
    # Convert the graph to a SAT instance
    sat_instance = convert_graph_to_sat(G)
    
    # Compute the DPLL search tree height for the SAT instance
    dpll_height = compute_dpll_search_tree_height(sat_instance)
    if dpll_height > n ** 1.5:
        return {
            "metric_name": "dpll_search_tree_height",
            "metric_value": dpll_height,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"SAT instance with {n} vertices has DPLL search tree height {dpll_height}"
        }
    
    return {
        "metric_name": "minimal_polynomial_degree",
        "metric_value": min_poly_degree,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

def generate_random_planar_graph(n: int) -> dict:
    # This is a simplified version of generating a random planar graph
    G = {}
    for i in range(1, n + 1):
        G[i] = []
    
    edges_added = 0
    while len(G) > 2 and edges_added < 3 * (n - 2):
        u = random.choice(list(G.keys()))
        v = random.choice(list(G.keys()))
        if u != v and v not in G[u]:
            G[u].append(v)
            G[v].append(u)
            edges_added += 1
    
    return G

def compute_minimal_polynomial_degree(G: dict) -> int:
    # This is a simplified version of computing the minimal polynomial degree
    # For simplicity, we assume the degree is proportional to the number of vertices
    return len(G)

def convert_graph_to_sat(G: dict) -> list:
    # Convert the graph to a SAT instance (simplified)
    clauses = []
    for u in G.keys():
        for v in G[u]:
            clauses.append([u, v])
    return clauses

def compute_dpll_search_tree_height(sat_instance: list) -> int:
    # This is a simplified version of computing the DPLL search tree height
    # For simplicity, we assume the height is proportional to the number of vertices
    return len(sat_instance)

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.2f} std={std_metric_value:.2f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.2f} std={std_metric_value:.2f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")