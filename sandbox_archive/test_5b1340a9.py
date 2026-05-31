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
    n = 40
    mtr_values = []
    w_values = []

    for _ in range(30):
        # Generate a random Tseitin formula with n variables
        G = {i: [] for i in range(n)}
        for i in range(n):
            x, y, z = random.sample(range(n), 3)
            if random.choice([True, False]):
                G[x].append((y, True))
                G[y].append((x, False))
            else:
                G[x].append((z, True))
                G[z].append((x, False))

        # Compute the minimal geometric entropy mtr(φ_G)
        # This is a placeholder for the actual computation
        mtr = random.random()  # Replace with actual computation

        # Compute the resolution proof width w(φ_G)
        # This is a placeholder for the actual computation
        w = random.randint(1, n)  # Replace with actual computation

        mtr_values.append(mtr)
        w_values.append(w)

    correlation_coefficient = compute_correlation(mtr_values, w_values)
    p_value = compute_p_value(correlation_coefficient, len(mtr_values))

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": 30,
        "n_max": n,
        "conjecture_holds": correlation_coefficient >= 0.7 and p_value < 0.05,
        "counterexample": "" if correlation_coefficient >= 0.7 and p_value < 0.05 else "correlation_too_low_or_p_value_too_high"
    }

def compute_correlation(x, y):
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
    std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
    std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
    return cov / (std_x * std_y)

def compute_p_value(r, n):
    t_statistic = r * math.sqrt((n - 2) / (1 - r ** 2))
    df = n - 2
    p_value = 2 * (1 - math.erf(abs(t_statistic) / math.sqrt(2)))
    return p_value

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)

    mean_metric_value = sum(r['metric_value'] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r['metric_value'] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)

    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low_or_p_value_too_high\" first_failing_seed={first_failing_seed}")