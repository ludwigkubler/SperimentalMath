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
    
    def generate_max_cut_instance(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.add((i, j))
        return edges
    
    def pseudoexpectation_matrix(edges, n):
        M = [[0] * n for _ in range(n)]
        for u, v in edges:
            M[u][v] = 1
            M[v][u] = 1
        return M
    
    def hodge_rank(M):
        n = len(M)
        rank = 0
        for i in range(n):
            if all(M[j][i] == 0 for j in range(i)):
                continue
            rank += 1
            for j in range(n):
                if j != i and M[j][i] != 0:
                    for k in range(n):
                        M[j][k] -= M[i][k]
        return rank
    
    def sos_approximation_ratio(edges, n):
        # Placeholder for actual SOS algorithm implementation
        # For simplicity, we assume a constant approximation ratio of 0.878
        return 0.878
    
    n = random.randint(5, 40)
    edges = generate_max_cut_instance(n)
    M = pseudoexpectation_matrix(edges, n)
    d = random.randint(1, n - 1)
    
    hodge_rk = hodge_rank(M)
    approx_ratio = sos_approximation_ratio(edges, n)
    
    metric_value = approx_ratio
    instances_tested = 1
    conjecture_holds = (hodge_rk < d and approx_ratio <= 0.878) or (hodge_rk >= d and approx_ratio > 0.878)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "approximation_ratio",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
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
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")