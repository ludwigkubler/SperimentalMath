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
    
    def generate_disjointness_matrix(n):
        M = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    M[i][j] = 1
                    M[j][i] = 1
        return M
    
    def spectral_radius(matrix):
        n = len(matrix)
        eigenvalues = []
        for _ in range(10):  # Power iteration method
            v = [random.random() for _ in range(n)]
            v /= sum(v)
            v_next = [sum(matrix[i][j] * v[j] for j in range(n)) for i in range(n)]
            v_next /= sum(v_next)
            eigenvalues.append(sum(v_next[i] * v[i] for i in range(n)))
        return max(eigenvalues)
    
    def semicircle_density(x):
        if -2 <= x <= 2:
            return (1 / math.pi) * math.sqrt(4 - x**2)
        else:
            return 0
    
    def free_entropy(matrix):
        n = len(matrix)
        rho = spectral_radius(matrix)
        integral = 0
        for i in range(n):
            for j in range(n):
                integral += semicircle_density((matrix[i][j] + 1) / 2)
        return -integral
    
    n = 16
    M = generate_disjointness_matrix(n)
    tau_M = free_entropy(M)
    
    metric_name = "free_entropy"
    metric_value = tau_M
    instances_tested = 1
    conjecture_holds = tau_M >= 0.3 * n
    counterexample = "" if conjecture_holds else f"tau_M={tau_M}, expected >= {0.3 * n}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]  # Default to first 30 primes
    
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
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")