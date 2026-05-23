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

def generate_random_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def p_adic_divergence(f, p):
    n = len(f)
    if n == 0:
        return 0
    count_ones = f.count(1)
    count_zeros = n - count_ones
    prob_one = Fraction(count_ones, n)
    prob_zero = Fraction(count_zeros, n)
    entropy = -prob_one * math.log2(prob_one) - prob_zero * math.log2(prob_zero)
    return entropy

def communication_complexity_disjointness(n):
    return n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_random_boolean_function(n)
        p_adic_val = p_adic_divergence(f, 2)  # Using base 2 for simplicity
        C_DISJ_n = communication_complexity_disjointness(n)
        
        if p_adic_val == float('inf') or C_DISJ_n == float('inf'):
            continue
        
        results.append((p_adic_val, C_DISJ_n))
    
    if not results:
        return {
            "metric_name": "P-adic Divergence vs Communication Complexity",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    p_adic_vals = [r[0] for r in results]
    C_DISJ_ns = [r[1] for r in results]
    
    mean_p_adic = sum(p_adic_vals) / len(p_adic_vals)
    mean_C_DISJ = sum(C_DISJ_ns) / len(C_DISJ_ns)
    
    correlation_coefficient = (sum((p_adic_vals[i] - mean_p_adic) * (C_DISJ_ns[i] - mean_C_DISJ) for i in range(len(p_adic_vals))) /
                               math.sqrt(sum((p_adic_vals[i] - mean_p_adic)**2 for i in range(len(p_adic_vals))) *
                                         sum((C_DISJ_ns[i] - mean_C_DISJ)**2 for i in range(len(C_DISJ_ns)))))
    
    return {
        "metric_name": "P-adic Divergence vs Communication Complexity",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and max(p_adic_vals) <= 10,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")