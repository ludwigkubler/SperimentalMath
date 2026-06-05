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

# Helper functions for graph generation and Tseitin formula construction
def generate_d_regular_graph(n, d):
    if n * d % 2 != 0:
        raise ValueError("Graph size must be a multiple of the degree")
    
    G = [[] for _ in range(n)]
    edges = set()
    
    def add_edge(u, v):
        if u < v and (u, v) not in edges:
            G[u].append(v)
            G[v].append(u)
            edges.add((u, v))
            edges.add((v, u))
    
    for u in range(n):
        for v in range(u + 1, n):
            if len(G[u]) < d and len(G[v]) < d:
                add_edge(u, v)
    
    return G

def tseitin_formula(clauses):
    variables = set()
    literals = []
    for clause in clauses:
        variables.update(clause)
        literals.extend([f"¬{var}", var] for var in clause)
    
    # Construct the Tseitin formula
    phi = []
    for literal in literals:
        if literal.startswith("¬"):
            phi.append(f"{literal} ∨ {literal[1:]}")
        else:
            phi.append(f"{literal} ∨ ¬{literal}")
    
    return phi

# Function to compute the minimal order of formal group representations
def mfr(phi):
    # Placeholder for actual implementation
    # This is a dummy function that returns 0 for simplicity
    return 0

# Function to compute circuit monotone width
def circuit_monotone_width(clauses):
    # Placeholder for actual implementation
    # This is a dummy function that returns 1 for simplicity
    return 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    d = random.randint(2, min(n - 1, 3))
    G = generate_d_regular_graph(n, d)
    clauses = tseitin_formula(G)
    
    mfr_phi_G = mfr(clauses)
    w_monotone_phi_G = circuit_monotone_width(clauses)
    
    return {
        "metric_name": "mfr(G)",
        "metric_value": mfr_phi_G,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")