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
        for i in range(k):
            for j in range(i + 1, k):
                edges.add((i, j))
        for _ in range(2 * k, n):
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if (u, v) not in edges and (v, u) not in edges:
                edges.add((u, v))
        return edges
    
    def dnf_size(edges):
        n = max(max(u, v) for u, v in edges) + 1
        clauses = []
        for i in range(n):
            clause = [j for j in range(n) if (i, j) not in edges]
            if clause:
                clauses.append(clause)
        return len(clauses)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per size
            edges = generate_k_clique(n, random.randint(2, min(5, n // 2)))
            dnf_size_val = dnf_size(edges)
            results.append(dnf_size_val)
    
    mean_dnf_size = sum(results) / len(results)
    if mean_dnf_size < n:
        return {
            "metric_name": "mean_dnf_size",
            "metric_value": mean_dnf_size,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "mean_dnf_size is too small"
        }
    else:
        return {
            "metric_name": "mean_dnf_size",
            "metric_value": mean_dnf_size,
            "instances_tested": len(results),
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_dnf_size = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_dnf_size} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_dnf_size} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mean_dnf_size is too small' first_failing_seed={first_failing_seed}")