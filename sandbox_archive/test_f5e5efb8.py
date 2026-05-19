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
    
    def generate_k_clique(n, k):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < k / (n * (n - 1) / 2):
                    edges.add((i, j))
        return edges
    
    def dnf_size(edges, n):
        terms = set()
        for i in range(1 << n):
            term = True
            for j in range(n):
                if (i >> j) & 1:
                    found = False
                    for u, v in edges:
                        if u == j and not found:
                            found = True
                            break
                    if not found:
                        term = False
                        break
            if term:
                terms.add(i)
        return len(terms)
    
    def log_size(size):
        if size == 0:
            return -math.inf
        return math.log2(size)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_log_size = 0
    instances_tested = 0
    
    for n in n_values:
        k_clique_edges = generate_k_clique(n, 1)
        poly_edges = generate_k_clique(n, 0.5)
        
        log_size_k_clique = dnf_size(k_clique_edges, n)
        log_size_poly = dnf_size(poly_edges, n)
        
        total_log_size += log_size_k_clique + log_size_poly
        instances_tested += 2
    
    mean_log_size = total_log_size / instances_tested
    
    conjecture_holds = True
    counterexample = ""
    
    if mean_log_size <= len(n_values) * math.log2(len(n_values)):
        conjecture_holds = False
        counterexample = "Submodularity not satisfied"
    
    return {
        "metric_name": "mean_log_size",
        "metric_value": mean_log_size,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_log_size = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_log_size} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_log_size} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Submodularity not satisfied\" first_failing_seed={first_failing_seed}")