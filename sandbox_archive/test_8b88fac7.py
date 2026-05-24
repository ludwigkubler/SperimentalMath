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
    G = {i: set() for i in range(n)}
    edges = [(i, j) for i in range(n) for j in range(i+1, n)]
    num_edges = random.randint(0, len(edges))
    selected_edges = random.sample(edges, num_edges)
    for u, v in selected_edges:
        G[u].add(v)
        G[v].add(u)
    return G

def compute_free_entropy(G):
    n = len(G)
    degrees = [len(G[i]) for i in range(n)]
    sum_degrees = sum(degrees)
    entropy = 0
    for degree in degrees:
        if degree > 0:
            p = Fraction(degree, sum_degrees)
            entropy -= p * math.log(p, n)
    return entropy

def compute_distinguishing_tensor_width(P, G):
    n = len(G)
    queue = [(i, {i}) for i in range(n)]
    visited = set()
    
    while queue:
        u, S = queue.pop(0)
        if u in visited:
            continue
        visited.add(u)
        
        for v in G[u]:
            if v not in S:
                new_S = S.union({v})
                queue.append((v, new_S))
    
    return len(visited)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        G = generate_random_graph(n)
        F_G = compute_free_entropy(G)
        
        if F_G <= 0:
            continue
        
        P_size = n
        P = [random.sample(range(n), 2) for _ in range(P_size)]
        
        ρ_P = compute_distinguishing_tensor_width(P, G)
        
        if ρ_P == 0:
            continue
        
        results.append({
            "n": n,
            "F_G": F_G,
            "ρ_P": ρ_P
        })
    
    if not results:
        return {
            "metric_name": "free_entropy_vs_distinguishing_tensor_width",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "no_valid_instances"
        }
    
    instances_tested = len(results)
    mean_F_G = sum(result["F_G"] for result in results) / instances_tested
    mean_ρ_P = sum(result["ρ_P"] for result in results) / instances_tested
    
    conjecture_holds = all(F_G <= math.log(ρ_P, 2) for F_G, ρ_P in zip([result["F_G"] for result in results], [result["ρ_P"] for result in results]))
    
    if not conjecture_holds:
        counterexample = "F(G) > log_2(ρ(P))"
        first_failing_seed = seed
    else:
        counterexample = ""
    
    return {
        "metric_name": "free_entropy_vs_distinguishing_tensor_width",
        "metric_value": mean_F_G,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))  # Default to first 30 primes
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_F_G = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_F_G = math.sqrt(sum((r["metric_value"] - mean_F_G) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_F_G} std={std_F_G} support_fraction={support_fraction}")
    elif any(r["counterexample"] == "F(G) > log_2(ρ(P))" for r in results):
        first_failing_seed = next(r["seed"] for r in results if r["counterexample"] == "F(G) > log_2(ρ(P))")
        print(f"RESULT: FALSIFIED counterexample=\"F(G) > log_2(ρ(P))\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_valid_instances")