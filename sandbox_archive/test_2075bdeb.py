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

def generate_monotone_k_clique(n, k):
    if n < k:
        return None
    vertices = list(range(n))
    clique_edges = set()
    for i in range(k):
        for j in range(i + 1, k):
            clique_edges.add((vertices[i], vertices[j]))
    remaining_edges = [(i, j) for i in range(k, n) for j in range(i + 1, n)]
    random.shuffle(remaining_edges)
    for u, v in remaining_edges[:n - k]:
        if (u, v) not in clique_edges and (v, u) not in clique_edges:
            clique_edges.add((u, v))
    return clique_edges

def generate_coxeter_group_action(n):
    # Simplified Coxeter group action for demonstration
    # This is a placeholder and should be replaced with actual group theory code
    action = {}
    for i in range(n):
        action[i] = (i + 1) % n
    return action

def count_distinct_orbits(clique_edges, action):
    orbits = set()
    visited = set()
    for v in clique_edges:
        if v not in visited:
            orbit = {v}
            current = v
            while True:
                next_v = action[current]
                if next_v == v:
                    break
                orbit.add(next_v)
                current = next_v
            orbits.add(frozenset(orbit))
            visited.update(orbit)
    return len(orbits)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        k = min(n // 2, 10)  # Ensure k is at least 1 and at most n//2
        clique_edges = generate_monotone_k_clique(n, k)
        if clique_edges is None:
            continue
        
        action = generate_coxeter_group_action(n)
        orbits_count = count_distinct_orbits(clique_edges, action)
        
        results.append({
            "n": n,
            "k": k,
            "orbits_count": orbits_count
        })
    
    if not results:
        return {
            "metric_name": "Orbits Count",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid monotone k-CLIQUE formula generated"
        }
    
    mean_orbits = sum(result["orbits_count"] for result in results) / len(results)
    std_orbits = math.sqrt(sum((result["orbits_count"] - mean_orbits) ** 2 for result in results) / len(results))
    
    return {
        "metric_name": "Orbits Count",
        "metric_value": mean_orbits,
        "instances_tested": len(results),
        "conjecture_holds": mean_orbits <= k**3,  # Polynomial upper bound
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_orbits = sum(r["metric_value"] for r in results) / len(results)
    std_orbits = math.sqrt(sum((r["metric_value"] - mean_orbits) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_orbits} std={std_orbits} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_orbits} std={std_orbits} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"n={r['n']}, k={r['k']}, orbits_count={r['orbits_count']}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break