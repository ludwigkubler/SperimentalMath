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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def permutation_representation(f):
        n = len(f)
        G_f = []
        for i in range(2**n):
            permuted = [f[i ^ (1 << j)] for j in range(n)]
            G_f.append(permuted)
        return G_f
    
    def automorphism_group(G_f):
        n = int(math.log2(len(G_f)))
        aut_group = []
        for i in range(1, 2**n):
            if all(G_f[i ^ (1 << j)] == G_f[j] for j in range(n)):
                aut_group.append(i)
        return aut_group
    
    def communication_complexity(f):
        n = len(f)
        # Simplified example: Hamming distance
        return sum(1 for i in range(2**n) if f[i] != f[i ^ 1])
    
    results = []
    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        G_f = permutation_representation(f)
        aut_group = automorphism_group(G_f)
        c_f = communication_complexity(f)
        results.append((n, len(aut_group), c_f))
    
    n_max = max(n for _, _, _ in results)
    if n_max < 16:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "n_max < 16"
        }
    
    C = [c for _, _, c in results]
    A = [a for _, a, _ in results]
    mean_C = sum(C) / len(C)
    mean_A = sum(A) / len(A)
    numerator = sum((C[i] - mean_C) * (A[i] - mean_A) for i in range(len(C)))
    denominator = math.sqrt(sum((C[i] - mean_C)**2 for i in range(len(C))) * sum((A[i] - mean_A)**2 for i in range(len(A))))
    if denominator == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "denominator is zero"
        }
    pearson_corr = numerator / denominator
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": pearson_corr >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{trial_result}...}}")
        results.append(trial_result)
    
    mean_corr = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std=None support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std=None support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")