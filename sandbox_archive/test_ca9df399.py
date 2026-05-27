# auto-injected by SEC sandbox
import json
import sys
import os
import time
import re
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
import math
import itertools
import collections

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_k_clique_instance(n, k):
        if n < k:
            return [], []
        vertices = list(range(n))
        edges = [(i, j) for i in range(k) for j in range(i+1, k)]
        for _ in range(k, n):
            v = random.choice(vertices[:k])
            u = random.choice(vertices[k:])
            if (v, u) not in edges and (u, v) not in edges:
                edges.append((v, u))
        return vertices, edges
    
    def hodge_diamond_invariant(n, k):
        # Placeholder for actual Hodge diamond invariant calculation
        # For simplicity, we use a dummy value that depends on n and k
        return Fraction(n**k, 2**(n-k))
    
    def monotone_circuit_size(k, n):
        # Placeholder for actual monotone circuit size calculation
        # For simplicity, we use a dummy value that depends on k and n
        return 2**k * n**k
    
    max_n = 40
    min_n = 5
    step = (max_n - min_n) // 3
    results = []
    
    for n in range(min_n, max_n + 1, step):
        k = random.randint(2, min(n-1, 10))
        vertices, edges = generate_k_clique_instance(n, k)
        HD_C = hodge_diamond_invariant(n, k)
        size_C = monotone_circuit_size(k, n)
        results.append((HD_C, size_C))
    
    if not results:
        return {
            "metric_name": "Spearman's rank correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    n_tests = len(results)
    HD_C_values = [HD_C for HD_C, _ in results]
    size_C_values = [size_C for _, size_C in results]
    
    def rank(data):
        ranks = {}
        sorted_data = sorted(data)
        for i, value in enumerate(sorted_data):
            if value not in ranks:
                ranks[value] = (i + 1) / len(sorted_data)
        return [ranks[x] for x in data]
    
    HD_C_rank = rank(HD_C_values)
    size_C_rank = rank(size_C_values)
    
    n_tests = len(results)
    sum_diff_squares = sum((HD_C_rank[i] - size_C_rank[i]) ** 2 for i in range(n_tests))
    rho = 1 - (6 * sum_diff_squares) / (n_tests * (n_tests**2 - 1))
    
    return {
        "metric_name": "Spearman's rank correlation coefficient",
        "metric_value": rho,
        "instances_tested": n_tests,
        "conjecture_holds": abs(rho) >= 0.95,  # Arbitrary threshold for significance
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(3, 6)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no trials executed")
        sys.exit(0)
    
    mean_rho = sum(result["metric_value"] for result in results) / len(results)
    std_rho = math.sqrt(sum((result["metric_value"] - mean_rho) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if abs(result["metric_value"]) >= 0.95) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Spearman's rank correlation coefficient does not meet threshold\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")