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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def matrix_representation(f):
        n = int(math.log2(len(f)))
        M_f = [[f[i * (1 << (j - 1)) + k] for k in range(1 << (j - 1))] for j in range(1, n + 1)]
        return M_f
    
    def geometric_entropy(M):
        support = [sum(row) for row in M if sum(row) > 0]
        if not support:
            return 0
        p = [x / sum(support) for x in support]
        entropy = -sum(p[i] * math.log2(p[i]) for i in range(len(p)))
        return entropy
    
    def communication_complexity_rank_variance(M):
        n = len(M)
        ranks = []
        for _ in range(100):  # Sample multiple times to get a good estimate
            permuted_M = [M[random.randint(0, n - 1)] for _ in range(n)]
            rank = sum(1 for i in range(n) if any(permuted_M[j][i] != M[j][i] for j in range(n)))
            ranks.append(rank)
        return statistics.variance(ranks)
    
    def f(n):
        # Example function that grows with n
        return n
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f_n = generate_boolean_function(n)
        M_f = matrix_representation(f_n)
        entropy = geometric_entropy(M_f)
        variance = communication_complexity_rank_variance(M_f)
        
        if variance == 0:
            continue
        
        ratio = entropy / (f(n) * variance)
        results.append({
            "n": n,
            "entropy": entropy,
            "variance": variance,
            "ratio": ratio
        })
    
    metric_value = sum(result["ratio"] for result in results) / len(results)
    instances_tested = len(results)
    n_max = max(result["n"] for result in results)
    conjecture_holds = all(abs(result["ratio"]) <= 1 for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Geometric Entropy Ratio",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = (sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")