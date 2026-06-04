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
        
        if u != v and (u, v) not in edges_added and (v, u) not in edges_added:
            graph[u].append(v)
            graph[v].append(u)
            edges_added.add((u, v))
    
    return graph

def calculate_moment_polytope(graph):
    n = len(graph)
    vertices = [tuple(sorted([i for i in range(n) if j in graph[i]])) for j in range(n)]
    polytope = set(vertices)
    
    while True:
        new_vertices = set()
        for v1, v2 in itertools.combinations(polytope, 2):
            v3 = tuple(sorted(set(v1) | set(v2)))
            if v3 not in polytope and all(len(set(v3).intersection(set(v))) == 1 for v in polytope):
                new_vertices.add(v3)
        if not new_vertices:
            break
        polytope.update(new_vertices)
    
    return polytope

def calculate_frege_proof_depth(formula):
    # Placeholder function. Replace with actual Frege proof depth calculation.
    return len(formula)  # Simplified for demonstration purposes

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        d = n // 2
        graph = generate_d_regular_graph(n, d)
        polytope = calculate_moment_polytope(graph)
        formula = tuple(sorted([i for i in range(n) if j in graph[i]]))  # Simplified for demonstration purposes
        proof_depth = calculate_frege_proof_depth(formula)
        
        results.append({
            "n": n,
            "d": d,
            "polytope_size": len(polytope),
            "proof_depth": proof_depth
        })
    
    if not results:
        return {
            "metric_name": "symplectic_leaves_vs_proof_depth",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_max = max(result["n"] for result in results)
    instances_tested = len(results)
    symplectic_leaves = [result["polytope_size"] for result in results]
    proof_depths = [result["proof_depth"] for result in results]
    
    # Calculate Spearman's rank correlation coefficient
    def rank(x):
        return {v: i + 1 for i, v in enumerate(sorted(set(x)))}
    
    rank_symplectic_leaves = rank(symplectic_leaves)
    rank_proof_depths = rank(proof_depths)
    
    n = len(rank_symplectic_leaves)
    sum_diff_ranks_squared = sum((rank_symplectic_leaves[i] - rank_proof_depths[i]) ** 2 for i in range(n))
    spearman_corr = 1 - (6 * sum_diff_ranks_squared) / (n * (n**2 - 1))
    
    # Calculate mean absolute difference
    mean_abs_diff = sum(abs(s - d) for s, d in zip(symplectic_leaves, proof_depths)) / n
    
    return {
        "metric_name": "symplectic_leaves_vs_proof_depth",
        "metric_value": spearman_corr,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": spearman_corr >= 0.8 and mean_abs_diff <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")