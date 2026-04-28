# auto-injected by SEC sandbox
import collections
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
import sys
import json
from itertools import product

def truth_table(f, n):
    return [f(i) for i in range(2**n)]

def lambda_2(T):
    asc = desc = 0
    for i in range(len(T)):
        if T[i] == 0:
            asc += sum(T[j] for j in range(i+1, len(T)) if T[j] == 1)
        else:
            desc += sum(T[j] for j in range(i+1, len(T)) if T[j] == 0)
    return abs(asc - desc)

def quine_mccluskey(f, n):
    # Simplified version of Quine–McCluskey algorithm
    minterms = [i for i in range(2**n) if f(i)]
    active = minterms.copy()
    prime_implicants = []
    while len(active) > 1:
        pairs = [(active[i], active[j]) for i in range(len(active)) for j in range(i+1, len(active))]
        new_active = []
        for pair in pairs:
            diff_count = sum(1 for a, b in zip(pair[0].to_bin(), pair[1].to_bin()) if a != b)
            if diff_count == 1:
                new_term = (pair[0] & pair[1]) << 1
                if new_term not in new_active:
                    new_active.append(new_term)
        active = new_active
    prime_implicants.extend(active)
    return len(prime_implicants)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [8, 10, 12, 14]
    results = []
    
    for n in n_values:
        for ensemble_type in ["random", "planted", "symmetric", "LTF"]:
            if ensemble_type == "random":
                f = lambda x: random.choice([0, 1])
                DNF_min_or_upper = 2**n
            elif ensemble_type == "planted":
                M = 2**(n-2)
                f = lambda x: sum((x >> i) & 1 for i in range(n)) >= M // 2
                DNF_min_or_upper = M
            elif ensemble_type == "symmetric":
                k = n // 2
                f = lambda x: sum((x >> i) & 1 for i in range(k)) >= k // 2
                DNF_min_or_upper = 2**k
            elif ensemble_type == "LTF":
                weights = [random.randint(1, 10) for _ in range(n)]
                f = lambda x: sum(w * ((x >> i) & 1) for i, w in enumerate(weights)) >= sum(weights) // 2
                DNF_min_or_upper = len([w for w in weights if w > 0])
            
            T = truth_table(f, n)
            lambda_2_val = lambda_2(T)
            log_lambda_2 = math.log2(1 + lambda_2_val)
            log_DNF_min_or_upper = math.log2(1 + DNF_min_or_upper)
            results.append((log_lambda_2, log_DNF_min_or_upper))
    
    if not results:
        return {
            "metric_name": "lambda_2 vs DNF_min",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    log_lambda_2_vals, log_DNF_min_or_upper_vals = zip(*results)
    slope = (sum(log_lambda_2_vals) - sum(log_DNF_min_or_upper_vals)) / len(results)
    conjecture_holds = all(log_lambda_2 <= n + log_DNF_min_or_upper + 5 * math.log2(n+1) for n, log_DNF_min_or_upper in zip(n_values, log_DNF_min_or_upper_vals))
    
    return {
        "metric_name": "lambda_2 vs DNF_min",
        "metric_value": slope,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Slope {slope} is outside expected range"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(json.dumps({"TRIAL": {"seed": seed, **result}}))
        results.append(result["metric_value"])
    
    mean_slope = sum(results) / len(results)
    std_slope = math.sqrt(sum((x - mean_slope)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r is not None and all(r <= n + 5 * math.log2(n+1) for n in [8, 10, 12, 14])) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_slope} std={std_slope} support_fraction={support_fraction}")
    elif any(r is not None and all(r > n + 5 * math.log2(n+1) for n in [8, 10, 12, 14]) for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result is not None and any(result > n + 5 * math.log2(n+1) for n in [8, 10, 12, 14]))
        print(f"RESULT: FALSIFIED counterexample=\"Slope outside expected range\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")