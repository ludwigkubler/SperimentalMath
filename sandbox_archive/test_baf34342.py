# auto-injected by SEC sandbox
import math
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
from itertools import combinations

def generate_3_regular_graph(n):
    if n % 2 != 0:
        raise ValueError("n must be even for a 3-regular graph")
    
    G = {i: {} for i in range(n)}
    degree = 3
    
    while True:
        edges = set()
        for u in range(n):
            available_neighbors = [v for v in range(n) if v != u and v not in G[u]]
            neighbors = random.sample(available_neighbors, degree)
            for v in neighbors:
                edges.add((min(u, v), max(u, v)))
        
        if len(edges) == n * degree // 2:
            break
    
    for (u, v) in edges:
        G[u][v] = 1
        G[v][u] = 1
    
    return G

def compute_cocycle_imbalance(G):
    n = len(G)
    min_bound = float('inf')
    
    for S in range(1, n):
        bound = abs(sum(G[u][v] for u, v in combinations(S, 2))) / min(len(S), n - len(S))
        if bound < min_bound:
            min_bound = bound
    
    return min_bound

def resolve_clause_set(clause_set, width):
    stack = []
    while clause_set:
        new_clause_set = set()
        for clause in clause_set:
            if any(lit not in stack and -lit not in stack for lit in clause):
                stack.append(random.choice(clause))
            else:
                new_clause_set.add(tuple(sorted(lit for lit in clause if lit not in stack and -lit not in stack)))
        clause_set = new_clause_set
        if len(stack) > width:
            return False
    return True

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [8, 10, 12, 14, 16, 18, 20]
    results = []
    
    for n in n_values:
        G = generate_3_regular_graph(n)
        c = {i: random.choice([0, 1]) for i in range(n)}
        
        I_G = compute_cocycle_imbalance(G)
        min_bound = float('inf')
        S_star = None
        
        for S in range(1, n):
            bound = abs(sum(G[u][v] for u, v in combinations(S, 2))) / min(len(S), n - len(S))
            if bound < min_bound:
                min_bound = bound
                S_star = S
        
        w_T_G_c = 0
        while not resolve_clause_set({(c[u] ^ c[v]) * (1 - G[u][v]) for u, v in G}, w_T_G_c):
            w_T_G_c += 1
        
        results.append({
            "n": n,
            "I(G)": I_G,
            "w(T(G,c))": w_T_G_c,
            "S*": S_star
        })
    
    total_instances = len(results)
    support_count = sum(1 for result in results if result["w(T(G,c))"] >= result["I(G)"] * min(len(result["S*"]), len(G) - len(result["S*"])) / 2 + 1)
    
    conjecture_holds = support_count == total_instances
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "resolution_width",
        "metric_value": sum(result["w(T(G,c))"] for result in results) / total_instances,
        "instances_tested": total_instances,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={sum(result['metric_value'] for result in results) / len(results)} std=0 support_fraction=1")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")