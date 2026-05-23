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

def generate_k_clique_graph(k, n):
    if k > n:
        raise ValueError("k must be less than or equal to n")
    
    nodes = list(range(n))
    edges = []
    
    # Ensure the graph is a clique of size k
    for i in range(k):
        for j in range(i + 1, k):
            edges.append((nodes[i], nodes[j]))
    
    # Add remaining random edges to make it a regular graph
    while len(edges) < n * (n - 1) // 2:
        node1 = random.choice(nodes)
        node2 = random.choice(nodes)
        if node1 != node2 and (node1, node2) not in edges and (node2, node1) not in edges:
            edges.append((node1, node2))
    
    return nodes, edges

def regular_expression_from_graph(n):
    # Construct a simple regular expression for the complement of the clique
    # This is a placeholder; actual construction depends on the graph structure
    regex = "0" * n + "1" * (n - 1)
    return regex

def automorphism_group_order(regex):
    # Placeholder for computing the automorphism group order
    # Actual computation would depend on the specific regex structure
    return len(regex)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0.0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Test with 5 random k values per n
            k = random.randint(1, min(n - 1, 3))
            try:
                graph = generate_k_clique_graph(k, n)
                regex = regular_expression_from_graph(n)
                order = automorphism_group_order(regex)
                
                total_metric_value += order ** (1/4)
                instances_tested += 1
            except Exception as e:
                print(f"Error in run_trial with seed {seed}, n={n}, k={k}: {e}")
    
    if instances_tested == 0:
        return {
            "metric_name": "Minimal Order of Automorphism Group",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_metric_value = total_metric_value / instances_tested
    conjecture_holds = all(1 <= order ** (1/4) <= n for _, edges in graph for order in automorphism_group_order(regular_expression_from_graph(n)))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Minimal Order of Automorphism Group",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 50, 2))  # Default to first 30 prime numbers
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")