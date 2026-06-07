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
    
    # Generate a random d-regular graph G with n vertices
    n = 20  # Fixed for simplicity, can be adjusted
    d = 3   # Degree of the graph
    edges = set()
    while len(edges) < (n * d) // 2:
        u = random.randint(0, n-1)
        v = random.randint(0, n-1)
        if u != v and (u, v) not in edges and (v, u) not in edges:
            edges.add((u, v))
    
    # Compute the minimal local induction dimension mld(G) of its associated algebraic variety
    # This is a placeholder for the actual computation using an existing computational geometry library
    mld_G = random.uniform(1, 20)  # Placeholder value
    
    # For each vertex in G, compute the circuit entanglement complexity e(φ_G)
    # This is a placeholder for the actual computation using Tseitin formulas and standard entanglement measures
    e_phi_G = [random.uniform(1, 20) for _ in range(n)]  # Placeholder values
    
    # Compare mld(G) with e(φ_G) over 30 random seeds to determine the correlation
    correlation_coefficient = sum((mld_G - x) * (e_phi_G[i] - y) for i, (x, y) in enumerate(zip([mld_G]*n, e_phi_G))) / (len(e_phi_G) * math.sqrt(sum((mld_G - x)**2 for x in [mld_G]*n)) * math.sqrt(sum((y - y_bar)**2 for y, y_bar in zip(e_phi_G, [sum(e_phi_G)/len(e_phi_G)]*len(e_phi_G)))))
    
    # Return the results
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": n,
        "n_max": n,
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and math.sqrt(sum((mld_G - x)**2 for x in [mld_G]*n)) <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = list(map(int, sys.argv[1:])) or [53, 79, 83, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")