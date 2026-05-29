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

def gaussian_sample():
    u1, u2 = random.random(), random.random()
    return -math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)

def min_plus_convolution(f, n):
    g = [float('inf')] * n
    for i in range(n):
        for j in range(n):
            k = (i + j) % n
            g[k] = min(g[k], f[i] + f[j])
    return g

def maslov_dequantized_tft(h, beta, n):
    exp_h = [math.exp(-beta * h[j]) for j in range(n)]
    sum_exp_h = sum(exp_h)
    tft_values = [-1 / beta * math.log(abs(sum_exp_h * math.exp(-2 * math.pi * 1j * k / n))) for k in range(n)]
    return min(tft_values)

def mfc(h, n):
    return min(abs(maslov_dequantized_tft(h, 5, n)) for k in range(1, n))

def delta(f, beta, n):
    g = min_plus_convolution(f, n)
    return abs(mfc(g, n) - 2 * mfc(f, n))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [8, 12, 16, 20, 24, 28, 32, 36, 40]:
        f = [gaussian_sample() for _ in range(n)]
        delta_value = delta(f, 5, n)
        results.append(delta_value)
    mean_delta = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean_delta) ** 2 for x in results) / len(results))
    support_fraction = all(x <= 4 * math.sqrt(math.log(n)) for n, x in zip([8, 12, 16, 20, 24, 28, 32, 36, 40], results))
    return {
        "metric_name": "delta",
        "metric_value": mean_delta,
        "instances_tested": len(results),
        "n_max": max([8, 12, 16, 20, 24, 28, 32, 36, 40]),
        "conjecture_holds": support_fraction,
        "counterexample": "" if support_fraction else "mean_delta > 4 * sqrt(log(n)) for some n"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    mean_result = sum(results) / len(results)
    std_dev_result = math.sqrt(sum((x - mean_result) ** 2 for x in results) / len(results))
    support_fraction = all(x <= 4 * math.sqrt(math.log(n)) for n, x in zip([8, 12, 16, 20, 24, 28, 32, 36, 40], results))
    if support_fraction:
        print(f"RESULT: SUPPORTED mean={mean_result} std={std_dev_result} support_fraction={support_fraction}")
    else:
        for seed in seeds:
            result = run_trial(seed)
            if not result["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"mean_delta > 4 * sqrt(log(n))\" first_failing_seed={seed}")
                break