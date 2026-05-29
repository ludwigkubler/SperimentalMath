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

def gaussian_sample(mu=0, sigma=1):
    u1 = random.random()
    u2 = random.random()
    z0 = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
    return mu + sigma * z0

def min_plus_convolution(f, g, n):
    result = [float('inf')] * n
    for i in range(n):
        for j in range(n):
            if (i + j) % n == 0:
                result[i] = min(result[i], f[i] + g[j])
    return result

def maslov_dequantized_tft(h, beta, n):
    h_min = min(h)
    h_shifted = [x - h_min for x in h]
    sum_exp_h = sum(math.exp(-beta * x) for x in h_shifted)
    tft_values = [-1 / beta * math.log(abs(sum_exp_h)) for _ in range(n)]
    return tft_values

def mfc(h, n):
    return min(abs(maslov_dequantized_tft(h, 5, n)) for k in range(1, n))

def delta(f, g, n):
    return abs(mfc(g, n) - 2 * mfc(f, n))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [8, 12, 16, 20, 24, 28, 32, 36, 40]
    results = []
    
    for n in n_values:
        f = [gaussian_sample() for _ in range(n)]
        g = min_plus_convolution(f, f, n)
        
        delta_value = delta(f, g, n)
        results.append(delta_value)
    
    mean_delta = sum(results) / len(results)
    std_dev_delta = math.sqrt(sum((x - mean_delta) ** 2 for x in results) / len(results))
    
    return {
        "metric_name": "Delta",
        "metric_value": mean_delta,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": all(x <= 4 * math.sqrt(math.log(n)) for n, x in zip(n_values, results)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    all_results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        all_results.append(trial_result)
    
    mean_delta = sum(x["metric_value"] for x in all_results) / len(all_results)
    std_dev_delta = math.sqrt(sum((x["metric_value"] - mean_delta) ** 2 for x in all_results) / len(all_results))
    support_fraction = sum(1 for x in all_results if x["conjecture_holds"]) / len(all_results)
    
    if all(x["conjecture_holds"] for x in all_results):
        print(f"RESULT: SUPPORTED mean={mean_delta} std={std_dev_delta} support_fraction={support_fraction}")
    elif any(not x["conjecture_holds"] for x in all_results) and support_fraction >= 0.8:
        print("RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed=<s>")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_data n_tested={len(all_results)}")