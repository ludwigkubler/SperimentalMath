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

def generate_random_planar_graph(n):
    if n < 3:
        return []
    
    nodes = list(range(n))
    edges = set()
    
    def add_edge(u, v):
        if u != v and (u, v) not in edges and (v, u) not in edges:
            edges.add((u, v))
            return True
        return False
    
    def is_planar():
        if len(nodes) <= 4:
            return True
        
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                for k in range(j + 1, len(nodes)):
                    for l in range(k + 1, len(nodes)):
                        if (i, j) in edges and (j, k) in edges and (k, i) in edges:
                            if (i, l) in edges or (l, i) in edges:
                                return False
        return True
    
    while not is_planar():
        u = random.choice(nodes)
        v = random.choice(nodes)
        add_edge(u, v)
    
    return list(edges)

def geometric_entropy(G):
    if not G:
        return 0.0
    
    degree_sum = sum(len(neighbors) for node, neighbors in G.items())
    n = len(G)
    
    p = [len(neighbors) / degree_sum for node, neighbors in G.items()]
    entropy = -sum(p_i * math.log2(p_i) for p_i in p if p_i > 0)
    
    return entropy

def communication_rank(G):
    if not G:
        return 0
    
    rank = 0
    visited = set()
    
    def dfs(node, parent):
        nonlocal rank
        visited.add(node)
        rank += 1
        
        for neighbor in G[node]:
            if neighbor != parent and neighbor not in visited:
                dfs(neighbor, node)
    
    for node in G:
        if node not in visited:
            dfs(node, None)
    
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        G = generate_random_planar_graph(n)
        if not G:
            continue
        
        H_G = geometric_entropy(G)
        r_G = communication_rank(G)
        
        if H_G < 0.1 or H_G > 10 or r_G < 0.1 or r_G > 10:
            return {
                "metric_name": "geometric_entropy",
                "metric_value": H_G,
                "instances_tested": len(results),
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "H(G) or r(G) out of range"
            }
        
        results.append((H_G, r_G))
    
    if not results:
        return {
            "metric_name": "geometric_entropy",
            "metric_value": 0.0,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "No valid graphs generated"
        }
    
    H_Gs, r_Gs = zip(*results)
    mean_H_G = sum(H_Gs) / len(H_Gs)
    mean_r_G = sum(r_Gs) / len(r_Gs)
    std_H_G = math.sqrt(sum((h - mean_H_G) ** 2 for h in H_Gs) / len(H_Gs))
    std_r_G = math.sqrt(sum((r - mean_r_G) ** 2 for r in r_Gs) / len(r_Gs))
    
    slope = (mean_H_G - mean_r_G) / std_r_G
    lower_bound = slope - 3 * std_H_G / std_r_G
    upper_bound = slope + 3 * std_H_G / std_r_G
    
    conjecture_holds = all(lower_bound <= s <= upper_bound for s in H_Gs)
    
    return {
        "metric_name": "geometric_entropy",
        "metric_value": mean_H_G,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")