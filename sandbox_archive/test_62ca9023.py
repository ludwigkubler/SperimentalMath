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
    C_v_k = v * (v - 1) // 2
    F_star_v = set()
    
    for S in combinations(range(v), k):
        minterm = frozenset(S)
        F_star_v.add(minterm)
    
    return F_star_v, C_v_k

def calculate_forman_ricci_curvature(edges, degrees):
    n_edges = len(edges)
    if n_edges == 0:
        return 0.0
    total_curvature = sum(4 - degrees[u] - degrees[v] for u, v in edges) / n_edges
    return total_curvature

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for v in [4, 10, 16, 20]:
        F_star_v, C_v_k = generate_clique_dnf(v)
        
        # Relabel vertices randomly
        relabeled_vertices = list(range(v))
        random.shuffle(relabeled_vertices)
        relabeled_F_star_v = {frozenset([relabeled_vertices[i] for i in S]) for S in F_star_v}
        
        # Build the graph G(F_star_v)
        n = len(relabeled_F_star_v)
        adjacency_matrix = [[0] * n for _ in range(n)]
        minterm_indices = {m: i for i, m in enumerate(relabeled_F_star_v)}
        
        for S in relabeled_F_star_v:
            for x in S:
                for y in range(v):
                    if y not in S and frozenset({x, y}) in relabeled_F_star_v:
                        u = minterm_indices[frozenset(S)]
                        v = minterm_indices[frozenset(S - {x} | {y})]
                        adjacency_matrix[u][v] = 1
                        adjacency_matrix[v][u] = 1
        
        # Calculate degrees and Forman-Ricci curvature
        degrees = [sum(row) for row in adjacency_matrix]
        forman_ricci_curvature = calculate_forman_ricci_curvature([(i, j) for i in range(n) for j in range(i+1, n) if adjacency_matrix[i][j]], degrees)
        
        results.append({
            "v": v,
            "C_v_k": C_v_k,
            "M_F_star_v": len(relabeled_F_star_v),
            "forman_ricci_curvature": forman_ricci_curvature,
            "predicted_bound": 4 - 2 * math.ceil(math.log2(v)) * (v - math.ceil(math.log2(v)))
        })
    
    metric_value = sum(result["M_F_star_v"] for result in results) / len(results)
    conjecture_holds = all(abs(result["forman_ricci_curvature"] - result["predicted_bound"]) <= 1 and result["M_F_star_v"] == result["C_v_k"] for result in results)
    
    return {
        "metric_name": "Forman-Ricci Regularity Bound",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "n_max": max(result["v"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "Forman-Ricci curvature or minterm count violated"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Forman-Ricci curvature or minterm count violated\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=budget_exceeded n_tested=30")