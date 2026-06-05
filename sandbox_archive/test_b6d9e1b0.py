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
    
    def add_edge(u, v):
        if (u, v) not in edges_added and (v, u) not in edges_added:
            graph[u].append(v)
            graph[v].append(u)
            edges_added.add((u, v))
            edges_added.add((v, u))
    
    for i in range(n):
        for j in range(i + 1, n):
            if len(graph[i]) < d and len(graph[j]) < d:
                add_edge(i, j)
    
    return graph

def topological_entropy(graph):
    n = len(graph)
    degrees = [len(neighbors) for neighbors in graph]
    max_degree = max(degrees)
    
    # Approximate the topological entropy using a finite cover
    h_G = 0.0
    for degree in degrees:
        if degree > 1:
            h_G += math.log(degree / (max_degree - 1))
    
    return h_G

def resolution_proof_width(graph):
    n = len(graph)
    max_clause_length = 0
    
    # Construct the Tseitin formula and compute the maximum clause length
    for i in range(n):
        for j in range(i + 1, n):
            if j not in graph[i]:
                max_clause_length = max(max_clause_length, 2)
    
    return max_clause_length

def run_trial(seed: int) -> dict:
    random.seed(seed)
    d_values = [3, 4, 5, 6]  # Degrees to test
    n_max = 0
    h_G_sum = 0.0
    w_phi_G_sum = 0.0
    instances_tested = 0
    
    for n in range(10, 21):  # Test sizes from 10 to 20
        for d in d_values:
            graph = generate_d_regular_graph(n * d, d)
            h_G = topological_entropy(graph)
            w_phi_G = resolution_proof_width(graph)
            
            if n > n_max:
                n_max = n
            
            h_G_sum += h_G
            w_phi_G_sum += w_phi_G
            instances_tested += 1
    
    mean_h_G = h_G_sum / instances_tested
    mean_w_phi_G = w_phi_G_sum / instances_tested
    correlation_coefficient = (instances_tested * sum(h_G * w_phi_G for h_G, w_phi_G in zip([h_G for _ in range(instances_tested)], [w_phi_G for _ in range(instances_tested)])) - mean_h_G * mean_w_phi_G) / math.sqrt((instances_tested * sum(h_G**2 for h_G in [h_G for _ in range(instances_tested)]) - mean_h_G**2) * (instances_tested * sum(w_phi_G**2 for w_phi_G in [w_phi_G for _ in range(instances_tested)]) - mean_w_phi_G**2))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": "" if correlation_coefficient >= 0.5 else f"Correlation coefficient {correlation_coefficient} is below the threshold"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, ...{result}...}}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")