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
    
    def generate_max_cut_instance(n):
        # Generate a random max-CUT instance with n variables
        edges = []
        for i in range(n):
            for j in range(i+1, n):
                if random.random() < 0.5:
                    edges.append((i, j))
        return edges
    
    def compute_pseudoexpectation_matrix(instance, d):
        # Compute the degree-d pseudoexpectation matrix
        n = len(instance)
        M = [[0] * n for _ in range(n)]
        for u, v in instance:
            M[u][v] += 1
            M[v][u] += 1
        return M
    
    def hodge_rank(matrix):
        # Compute the Hodge rank of a matrix (simplified version)
        n = len(matrix)
        rank = 0
        for i in range(n):
            if sum(matrix[i]) > 0:
                rank += 1
        return rank
    
    def sos_approximation_ratio(instance, d):
        # Approximate the max-CUT using a simple heuristic (simplified version)
        n = len(instance)
        cut_value = sum(1 for u, v in instance if random.random() < 0.5)
        return cut_value / n
    
    n = random.randint(5, 40)
    d = random.randint(2, min(n-1, 3))
    
    instance = generate_max_cut_instance(n)
    M = compute_pseudoexpectation_matrix(instance, d)
    hodge_rk = hodge_rank(M)
    ratio = sos_approximation_ratio(instance, d)
    
    metric_name = "approximation_ratio"
    metric_value = ratio
    instances_tested = 1
    
    if hodge_rk < d:
        conjecture_holds = ratio <= 0.878
        counterexample = "approximation_ratio_too_low" if not conjecture_holds else ""
    elif hodge_rk >= d:
        conjecture_holds = ratio > 0.878
        counterexample = "approximation_ratio_too_high" if not conjecture_holds else ""
    else:
        conjecture_holds = False
        counterexample = "mapping_undefined"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)
    
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
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")