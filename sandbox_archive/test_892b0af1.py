# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations, permutations

def generate_clique_dnf(v):
    k = math.ceil(math.log2(v))
    cliques = list(combinations(range(v), k))
    minterms = [frozenset(clique) for clique in cliques]
    return minterms

def compute_degree(graph, node):
    return sum(1 for neighbor in graph[node] if neighbor != node)

def compute_forman_ricci_curvature(graph):
    n_edges = sum(len(neighbors) for neighbors in graph.values()) // 2
    curvature_sum = sum(4 - deg_u - deg_w for u in graph for w in graph[u] if u < w)
    return curvature_sum / (2 * n_edges)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for v in [4, 10, 16, 20]:
        k = math.ceil(math.log2(v))
        minterms = generate_clique_dnf(v)
        
        # Relabel vertices randomly
        relabeling = list(permutations(range(v)))
        graph = {i: set() for i in range(len(minterms))}
        for u, minterm in enumerate(minterms):
            for v in range(u + 1, len(minterms)):
                shared_edges = minterm & minterms[v]
                if len(shared_edges) == k - 1:
                    graph[u].add(v)
                    graph[v].add(u)
        
        M_Fv = len(minterms)
        predicted_bound = 4 - 2 * k * (v - k)
        curvature = compute_forman_ricci_curvature(graph)
        
        results.append({
            "metric_name": "M(F_v)",
            "metric_value": M_Fv,
            "instances_tested": len(minterms),
            "n_max": v,
            "conjecture_holds": M_Fv == C(v, k) and abs(curvature - predicted_bound) <= 1,
            "counterexample": ""
        })
    
    return {
        "seed": seed,
        "results": results
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    all_results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        all_results.extend(trial_result["results"])
    
    metric_values = [result["metric_value"] for result in all_results]
    conjecture_holds = all(result["conjecture_holds"] for result in all_results)
    
    if conjecture_holds:
        mean_metric = sum(metric_values) / len(metric_values)
        std_metric = (sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values)) ** 0.5
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(all_results) if not result["conjecture_holds"])
        counterexample = all_results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")