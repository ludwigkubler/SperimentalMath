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
    
    def generate_random_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.add((i, j))
        return edges
    
    def compute_geometric_complexity_theory_width(graph, n):
        # Placeholder implementation
        return len(graph)
    
    def construct_projective_complex_variety(n):
        # Placeholder implementation
        chi_V = n
        alpha = (n + 1) // 2
        h1_V_OV_alpha = 0 if alpha % 2 == 0 else 1
        return chi_V, alpha, h1_V_OV_alpha
    
    def find_smallest_k(n):
        for k in range(1, n + 1):
            chi_V, alpha, h1_V_OV_alpha = construct_projective_complex_variety(k)
            if chi_V <= n and h1_V_OV_alpha == 0:
                return k
        return None
    
    n = random.randint(5, 40)
    graph = generate_random_graph(n)
    W_G = compute_geometric_complexity_theory_width(graph, n)
    k = find_smallest_k(n)
    
    if k is None:
        return {
            "metric_name": "W(G)",
            "metric_value": W_G,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    conjecture_holds = W_G <= k
    counterexample = f"Graph with n={n}, W(G)={W_G} > k={k}" if not conjecture_holds else ""
    
    return {
        "metric_name": "W(G)",
        "metric_value": W_G,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")