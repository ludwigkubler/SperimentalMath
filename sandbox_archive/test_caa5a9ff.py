# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import itertools
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank_variance(f):
        n = len(f).bit_length() - 1
        rank_matrix = [[f[i ^ (a & (1 << j))] == f[i ^ (b & (1 << j))] for j in range(n)] for a, b in itertools.combinations(range(2**n), 2)]
        rank_sum = sum(sum(row) for row in rank_matrix)
        rank_variance = Fraction(rank_sum, len(rank_matrix)**2)
        return rank_variance
    
    def quaternionic_automorphisms(f):
        n = len(f).bit_length() - 1
        aut_q = set()
        for a in range(2**n):
            if all(f[i ^ (a & (1 << j))] == f[i] for i in range(2**n) for j in range(n)):
                aut_q.add(a)
        return len(aut_q)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        f = generate_boolean_function(n)
        C_f = communication_complexity_rank_variance(f)
        aut_q_count = quaternionic_automorphisms(f)
        results.append((n, aut_q_count, C_f))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_max = max(n for _, _, _ in results)
    aut_q_values = [aut_q_count for _, aut_q_count, _ in results]
    C_f_values = [C_f for _, _, C_f in results]
    
    if n_max < 16:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "n_max_too_low"
        }
    
    mean_aut_q = sum(aut_q_values) / len(aut_q_values)
    mean_C_f = sum(C_f_values) / len(C_f_values)
    correlation_coefficient = sum((aut_q - mean_aut_q) * (C_f**0.5 - mean_C_f) for aut_q, C_f in zip(aut_q_values, C_f_values)) / (len(results) * (sum((aut_q - mean_aut_q)**2 for aut_q in aut_q_values) ** 0.5) * (sum((C_f**0.5 - mean_C_f)**2 for C_f in C_f_values) ** 0.5))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient > 0.7 and all(correlation_coefficient >= 0.5 for _ in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    all_results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        all_results.append(trial_result)
    
    if not all_results:
        print("RESULT: INCONCLUSIVE no_trials_run")
        exit(0)
    
    mean_metric_value = sum(result["metric_value"] for result in all_results) / len(all_results)
    std_metric_value = (sum((result["metric_value"] - mean_metric_value)**2 for result in all_results) / len(all_results))**0.5
    support_fraction = sum(1 for result in all_results if result["conjecture_holds"]) / len(all_results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in all_results):
        first_failing_seed = next(seed for seed, result in zip(seeds, all_results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")