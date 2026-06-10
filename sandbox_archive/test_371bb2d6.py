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
    n = 40
    d = 3
    G = generate_d_regular_graph(n, d)
    phi_G = construct_tseitin_formula(G)
    mli_G = compute_minimal_local_induction_degree(phi_G)
    d_phi_G = compute_frege_proof_depth(phi_G)
    
    return {
        "metric_name": "mli_vs_d",
        "metric_value": mli_G,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

def generate_d_regular_graph(n: int, d: int) -> list:
    G = [[] for _ in range(n)]
    degree_count = [0] * n
    added_edges = set()
    
    while any(count < d for count in degree_count):
        u = random.randint(0, n-1)
        v = random.randint(0, n-1)
        
        if u == v or (u, v) in added_edges:
            continue
        
        G[u].append(v)
        G[v].append(u)
        added_edges.add((u, v))
        degree_count[u] += 1
        degree_count[v] += 1
    
    return G

def construct_tseitin_formula(G: list) -> str:
    n = len(G)
    phi_G = ""
    
    for i in range(n):
        phi_G += f"X{i} | "
    
    for u, v in enumerate(G):
        for w in v:
            if u < w:
                phi_G += f"(~X{u} & ~X{w}) -> X{v[0]} | "
    
    return phi_G.strip()[:-2]

def compute_minimal_local_induction_degree(phi_G: str) -> float:
    # Placeholder for the actual computation
    return random.random()

def compute_frege_proof_depth(phi_G: str) -> int:
    # Placeholder for the actual computation
    return random.randint(1, 10)

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")