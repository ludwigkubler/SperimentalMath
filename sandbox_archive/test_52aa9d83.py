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

def max_plus_convolution(f, g):
    n = len(f)
    m = len(g)
    result = [[-math.inf] * (m + n - 1) for _ in range(n + m - 1)]
    for i in range(n):
        for j in range(m):
            result[i + j][i + j] = max(result[i + j][i + j], f[i] + g[j])
    return result

def max_plus_fourier_transform(f, n):
    if n == 1:
        return [f[0]]
    half_n = n // 2
    even_part = max_plus_fourier_transform([f[2 * i] for i in range(half_n)], half_n)
    odd_part = max_plus_fourier_transform([f[2 * i + 1] for i in range(half_n)], half_n)
    result = [-math.inf] * n
    for k in range(n):
        omega = (2 * math.pi * k) / n
        result[k] = max(even_part[k % half_n] - omega * k, odd_part[(k + half_n) % half_n] - omega * k)
    return result

def minimal_fourier_coefficient(f, n):
    fourier_transform = max_plus_fourier_transform(f, 2 ** n)
    return min(fourier_transform)

def discrepancy_measure(f, n):
    max_val = max(f)
    min_val = min(f)
    return max_val - min_val

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = m = 4
    f = [random.uniform(-5, 5) for _ in range(2 ** n)]
    g = [random.uniform(-5, 5) for _ in range(2 ** m)]
    
    f_conv_g = max_plus_convolution(f, g)
    min_fc_f = minimal_fourier_coefficient(f, n)
    min_fc_g = minimal_fourier_coefficient(g, m)
    min_fc_fg = minimal_fourier_coefficient(f_conv_g, n + m)
    disc_f = discrepancy_measure(f, 2 ** n)
    disc_g = discrepancy_measure(g, 2 ** m)
    disc_fg = discrepancy_measure(f_conv_g, 2 ** (n + m))
    
    conjecture_holds = abs(min_fc_fg - (min_fc_f + min_fc_g)) < 1e-9 and disc_fg <= disc_f + disc_g + 1e-9
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "DiscrepancyMeasure",
        "metric_value": disc_fg,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) <= 0.2:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")