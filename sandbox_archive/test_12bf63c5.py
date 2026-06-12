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

def binary_representation(x, n):
    return [(x >> i) & 1 for i in range(n-1, -1, -1)]

def p_adic_divergence(f):
    n = int(math.log2(len(f)))
    count = [0] * (1 << n)
    total = 0
    for x in range(1 << n):
        count[x] += f[x]
        total += f[x]
    mean = Fraction(total, 1 << n)
    variance = sum((count[x] - mean) ** 2 for x in range(1 << n)) / (1 << n)
    return math.sqrt(variance)

def communication_complexity_rank_variance(f):
    n = int(math.log2(len(f)))
    rank_variances = []
    for i in range(n):
        rank = 0
        for j in range(1 << n):
            if f[j] != 0:
                rank += 1
        rank_variances.append(rank)
    return sum((rank_variances[i] - sum(rank_variances) / n) ** 2 for i in range(n)) / n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        if n_max < n:
            break
        instances_tested = 0
        p_adic_vals = []
        rank_variances = []
        for _ in range(30):
            f = generate_random_boolean_function(n)
            p_adic_val = p_adic_divergence(f)
            rank_variance = communication_complexity_rank_variance(f)
            p_adic_vals.append(p_adic_val)
            rank_variances.append(rank_variance)
            instances_tested += 1
        if len(p_adic_vals) < 30:
            continue
        correlation_coefficient = sum((p_adic_vals[i] - mean_p_adic) * (rank_variances[i] - mean_rank_variance) for i in range(len(p_adic_vals))) / (len(p_adic_vals) * math.sqrt(variance_p_adic * variance_rank_variance))
        results.append({
            "n": n,
            "p_adic_vals": p_adic_vals,
            "rank_variances": rank_variances,
            "correlation_coefficient": correlation_coefficient
        })
    if not results:
        return {
            "metric_name": "Correlation Coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "No trials completed"
        }
    mean_correlation = sum(result["correlation_coefficient"] for result in results) / len(results)
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": mean_correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": all(result["correlation_coefficient"] >= 0.5 for result in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(30)]
    n_max = 40
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        if result["conjecture_holds"]:
            results.append(result["metric_value"])
    mean_metric_value = sum(results) / len(results) if results else None
    support_fraction = len([r for r in results if r >= 0.7]) / len(results) if results else None
    if all(r >= 0.7 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={math.sqrt(sum((r - mean_metric_value) ** 2 for r in results) / len(results))} support_fraction={support_fraction}")
    elif any(r < 0.5 for r in results):
        first_failing_seed = seeds[results.index(next(r for r in results if r < 0.5))]
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_below_0.5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_trials_completed")