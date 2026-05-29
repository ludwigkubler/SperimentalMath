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

def gaussian_sample():
    u1 = random.random()
    u2 = random.random()
    z0 = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
    return z0

def gaussian_vector(n):
    return [gaussian_sample() for _ in range(n)]

def min_plus_convolution(f, g, n):
    result = [float('inf')] * n
    for i in range(n):
        for j in range(n):
            result[(i + j) % n] = min(result[(i + j) % n], f[i] + g[j])
    return result

def maslov_dequantized_tft(h, beta, n):
    h_min = min(h)
    h_shifted = [x - h_min for x in h]
    sum_exp_h = sum(math.exp(-beta * x) for x in h_shifted)
    tft_values = [-1 / beta * math.log(abs(sum_exp_h * math.exp(-2 * math.pi * 1j * k / n))) for k in range(n)]
    return min(tft_values)

def mfc(h, n):
    return min(abs(maslov_dequantized_tft(h, 5, n)) for k in range(1, n))

def delta(f, beta, n):
    g = min_plus_convolution(f, f, n)
    return abs(mfc(g, n) - 2 * mfc(f, n))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [8, 12, 16, 20, 24, 28, 32, 36, 40]:
        f = gaussian_vector(n)
        delta_value = delta(f, 5, n)
        results.append(delta_value)
    
    mean_delta = sum(results) / len(results)
    support_fraction = all(mean_delta <= 4 * math.sqrt(math.log(n)) for n in [8, 12, 16, 20, 24, 28, 32, 36, 40])
    
    return {
        "metric_name": "mean_delta",
        "metric_value": mean_delta,
        "instances_tested": len(results),
        "n_max": max([8, 12, 16, 20, 24, 28, 32, 36, 40]),
        "conjecture_holds": support_fraction,
        "counterexample": "" if support_fraction else "mean_delta > 4 * sqrt(log(n)) for some n"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")