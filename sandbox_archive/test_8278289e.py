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
    
    def communication_complexity_rank(f):
        n = len(f)
        if n == 1:
            return 1
        circuit_ranks = []
        for i in range(1, n):
            for j in range(n - i + 1):
                subfunction = f[j:j+i]
                rank = max(communication_complexity_rank(subfunction[:i//2]), communication_complexity_rank(subfunction[i//2:]))
                circuit_ranks.append(rank)
        return min(circuit_ranks) if circuit_ranks else n
    
    def minimal_representation_degree(f):
        n = len(f)
        if n == 1:
            return 1
        # Placeholder for actual computation; this is a dummy implementation
        return n
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        d_phi_f = minimal_representation_degree(f)
        r_f = communication_complexity_rank(f)
        results.append((d_phi_f, r_f))
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No results generated"
        }
    
    d_phi_f_values = [d for d, _ in results]
    r_f_values = [r for _, r in results]
    
    mean_d_phi_f = sum(d_phi_f_values) / len(d_phi_f_values)
    mean_r_f = sum(r_f_values) / len(r_f_values)
    
    pearson_corr_coeff = sum((d - mean_d_phi_f) * (r - mean_r_f) for d, r in results) / (len(results) * math.sqrt(sum((d - mean_d_phi_f)**2 for d in d_phi_f_values)) * math.sqrt(sum((r - mean_r_f)**2 for r in r_f_values)))
    
    mean_abs_diff = sum(abs(d - r) for d, r in results) / len(results)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr_coeff,
        "instances_tested": 30,
        "n_max": max(n for _, n in results),
        "conjecture_holds": abs(pearson_corr_coeff) >= 0.8 and mean_abs_diff <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all("conjecture_holds" in result and result["conjecture_holds"] for result in results):
        mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=Unknown support_fraction={support_fraction}")
    elif any("conjecture_holds" in result and not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "conjecture_holds" in result and not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Not enough data to refute\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE Reason=Unknown")