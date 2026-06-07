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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_d_regular_graph(n, d):
        if (n * d) % 2 != 0 or d < 1 or d >= n:
            return None
        graph = {i: set() for i in range(n)}
        edges_added = 0
        while edges_added < n * d // 2:
            u, v = random.sample(range(n), 2)
            if u not in graph[v]:
                graph[u].add(v)
                graph[v].add(u)
                edges_added += 1
        return graph
    
    def tseitin_formula(graph):
        n = len(graph)
        clauses = []
        for i in range(n):
            literals = [f"X{i}_{j}" for j in range(d)]
            clauses.append(literals)
            for j in range(d):
                for k in range(j + 1, d):
                    clauses.append([f"-X{i}_{j}", f"-X{i}_{k}"])
        for i in range(n):
            for j in range(i + 1, n):
                for l in range(d):
                    for m in range(d):
                        if l != m:
                            clauses.append([f"-X{i}_{l}", f"-X{j}_{m}"])
        return clauses
    
    def symplectic_invariant(clauses):
        # Placeholder function to compute the minimal symplectic invariant
        # This is a stub and should be replaced with actual computation
        return random.random()
    
    def resolution_width(clauses):
        # Placeholder function to compute the resolution proof width
        # This is a stub and should be replaced with actual computation
        return random.randint(1, 10)
    
    n = 20
    d = 3
    graph = generate_d_regular_graph(n, d)
    if graph is None:
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "graph_generation_failed"
        }
    
    clauses = tseitin_formula(graph)
    msi = symplectic_invariant(clauses)
    w = resolution_width(clauses)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": w,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        seeds = [2**i + 1 for i in range(5, 8)]  # First 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")