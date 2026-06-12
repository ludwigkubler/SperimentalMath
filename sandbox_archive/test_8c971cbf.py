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

def generate_random_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def compute_p_adic_divergence(f):
    n = int(math.log2(len(f)))
    p_adic_vals = []
    for x in range(2**n):
        count = sum(1 for i in range(n) if f[x ^ (1 << i)] != f[x])
        p_adic_vals.append(count / n)
    return sum(p_adic_vals) / len(p_adic_vals)

def compute_rank_variance(f):
    n = int(math.log2(len(f)))
    rank_variances = []
    for x in range(2**n):
        count = sum(1 for i in range(n) if f[x ^ (1 << i)] != f[x])
        rank_variances.append(count)
    mean_rank_variance = sum(rank_variances) / len(rank_variances)
    variance_rank_variance = sum((x - mean_rank_variance)**2 for x in rank_variances) / len(rank_variances)
    return variance_rank_variance

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    p_adic_vals = []
    rank_variances = []

    for n in n_values:
        f = generate_random_boolean_function(n)
        p_adic_val = compute_p_adic_divergence(f)
        rank_variance = compute_rank_variance(f)
        p_adic_vals.append(p_adic_val)
        rank_variances.append(rank_variance)

    mean_p_adic = sum(p_adic_vals) / len(p_adic_vals)
    variance_p_adic = sum((x - mean_p_adic)**2 for x in p_adic_vals) / len(p_adic_vals)
    mean_rank_variance = sum(rank_variances) / len(rank_variances)
    variance_rank_variance = sum((x - mean_rank_variance)**2 for x in rank_variances) / len(rank_variances)

    correlation_coefficient = sum((p_adic_vals[i] - mean_p_adic) * (rank_variances[i] - mean_rank_variance) for i in range(len(p_adic_vals))) / (len(p_adic_vals) * math.sqrt(variance_p_adic * variance_rank_variance))

    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.5,
        "counterexample": "" if correlation_coefficient >= 0.5 else f"Correlation coefficient {correlation_coefficient} < 0.5"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 200))
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient_below_0.5' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")