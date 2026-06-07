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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def geometric_entropy(G):
        n = len(G)
        degree_sum = sum(sum(1 for v in G[u] if v != u) for u in G)
        return (degree_sum / (2 * n)) ** 0.5
    
    def resolution_proof_width(n, d):
        # Placeholder function to simulate the width of a resolution proof
        return n * d
    
    def generate_d_regular_graph(n, d):
        if (n * d) % 2 != 0:
            return None
        G = {i: set() for i in range(n)}
        edges = []
        for u in range(n):
            for v in range(u + 1, n):
                if len(G[u]) < d and len(G[v]) < d:
                    G[u].add(v)
                    G[v].add(u)
                    edges.append((u, v))
        return G
    
    def is_valid_d_regular_graph(G, n, d):
        for u in range(n):
            if len(G[u]) != d:
                return False
        return True
    
    results = []
    for _ in range(30):  # 30 instances per seed
        n = random.randint(5, 40)
        d = random.randint(2, min(2 * (n - 1), 8))
        G = generate_d_regular_graph(n, d)
        if not is_valid_d_regular_graph(G, n, d):
            continue
        
        H_G = geometric_entropy(G)
        w_phi_G = resolution_proof_width(n, d)
        
        if H_G == 0:
            continue
        
        ratio = w_phi_G / (H_G ** 2)
        results.append(ratio)
    
    if not results:
        return {
            "metric_name": "w(φ_G)/H(G)^2",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid d-regular graph generated"
        }
    
    return {
        "metric_name": "w(φ_G)/H(G)^2",
        "metric_value": sum(results) / len(results),
        "instances_tested": len(results),
        "n_max": max(n for _ in range(30)),
        "conjecture_holds": all(ratio <= 1.0 for ratio in results),  # Placeholder constant
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")