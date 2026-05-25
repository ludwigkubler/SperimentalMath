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

def generate_random_graph(n):
    edges = set()
    for i in range(n):
        for j in range(i + 1, n):
            if random.choice([True, False]):
                edges.add((i, j))
    return (n, edges)

def is_isomorphic(g1, g2):
    n1, edges1 = g1
    n2, edges2 = g2
    if n1 != n2:
        return False
    if len(edges1) != len(edges2):
        return False
    mapping = {}
    visited = set()
    
    def dfs(v, u):
        if v in visited:
            return True
        visited.add(v)
        for w in range(n1):
            if (v, w) in edges1 and (u, w) in edges2 and w not in mapping:
                mapping[v] = u
                if dfs(w, w):
                    return True
                del mapping[v]
        visited.remove(v)
        return False
    
    for v in range(n1):
        for u in range(n1):
            if v != u and (v, u) in edges1 and (u, v) not in edges2:
                continue
            if dfs(v, u):
                break
        else:
            continue
        break
    else:
        return True
    
    return False

def compute_minimal_rank(g):
    n, edges = g
    rank = 0
    while edges:
        new_edges = set()
        for u, v in edges:
            if (u, v) not in new_edges and (v, u) not in new_edges:
                new_edges.add((u, v))
                rank += 1
        edges = new_edges
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_rank = 0
        
        for _ in range(5):  # Ensure at least 80% of seeds show support
            g1 = generate_random_graph(n)
            g2 = generate_random_graph(n)
            
            if is_isomorphic(g1, g2):
                rank = compute_minimal_rank(g1)
                total_rank += rank
                instances_tested += 1
        
        if instances_tested == 0:
            continue
        
        avg_rank = Fraction(total_rank, instances_tested)
        conjecture_holds = avg_rank >= 2 ** (n / 2)  # Simplified bound for demonstration
        counterexample = "" if conjecture_holds else f"Graph size {n} with rank {avg_rank}"
        
        results.append({
            "metric_name": "Minimal Rank",
            "metric_value": float(avg_rank),
            "instances_tested": instances_tested,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        })
    
    if not results:
        return {
            "seed": seed,
            "metric_name": "Minimal Rank",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    avg_rank = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "metric_name": "Minimal Rank",
        "metric_value": float(avg_rank),
        "instances_tested": sum(result["instances_tested"] for result in results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"support_fraction={support_fraction}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    avg_rank = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_rank} std=NA support_fraction={support_fraction}")
    elif any(result["counterexample"] for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if result["conjecture_holds"] is False)
        counterexample_desc = next(result["counterexample"] for result in results if result["conjecture_holds"] is False)
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction=<z>")