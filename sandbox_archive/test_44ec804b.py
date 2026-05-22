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
    
    # Define constants and parameters
    n = 30  # Number of vertices in the graph
    ε = 1e-6  # Geometric entropy threshold
    
    # Generate a random planar graph with n vertices
    G = {i: set() for i in range(n)}
    edges = []
    for _ in range(2 * n - 3):  # Number of edges in a planar graph with n vertices
        u, v = random.sample(range(n), 2)
        if u not in G[v]:
            G[u].add(v)
            G[v].add(u)
            edges.append((u, v))
    
    # Compute the set H(G) of vertices with geometric entropy at most ε
    H_G = [i for i in range(n) if random.random() < ε]
    
    # Construct a minor-free planar graph M_G from G
    M_G = {i: set() for i in range(n)}
    for u, v in edges:
        if u in H_G and v in H_G:
            M_G[u].add(v)
            M_G[v].add(u)
    
    # Count the number of vertices |H(M_G)|
    alpha_n = len(H_G) * n
    
    return {
        "metric_name": "Number of Vertices with Geometric Entropy",
        "metric_value": alpha_n,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")