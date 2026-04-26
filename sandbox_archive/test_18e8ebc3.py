# auto-injected by SEC sandbox
import itertools
import collections
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
import json

def max_plus(a, b):
    return max(a, b)

def min_plus(a, b):
    return min(a, b)

def max_plus_fourier_transform(f, n):
    if n == 1:
        return f[0]
    half_n = n // 2
    even_part = max_plus_fourier_transform([f[2 * i] for i in range(half_n)], half_n)
    odd_part = max_plus_fourier_transform([f[2 * i + 1] for i in range(half_n)], half_n)
    result = [0] * n
    for k in range(n):
        if k < half_n:
            result[k] = max_plus(even_part[k], odd_part[(k - half_n) % half_n])
        else:
            result[k] = min_plus(even_part[k - half_n], odd_part[k - half_n])
    return result

def minimal_fourier_coefficient(f, n):
    fourier_transform = max_plus_fourier_transform(f, 2 ** n)
    return min(fourier_transform)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n, m = 4, 4
    f_coeffs = [random.uniform(-5, 5) for _ in range(1 << n)]
    g_coeffs = [random.uniform(-5, 5) for _ in range(1 << m)]
    
    def tropical_polynomial(f, x):
        return sum(f[i] * (-x[i]) for i in range(len(x)))
    
    f_conv_g = [0] * (1 << (n + m))
    for x in range(1 << n):
        for y in range(1 << m):
            f_val = tropical_polynomial(f_coeffs, list(bin(x)[2:].zfill(n)))
            g_val = tropical_polynomial(g_coeffs, list(bin(y)[2:].zfill(m)))
            f_conv_g[x * (1 << m) + y] = max_plus(f_val + g_val, -x - y)
    
    min_fc_f = minimal_fourier_coefficient(f_coeffs, n)
    min_fc_g = minimal_fourier_coefficient(g_coeffs, m)
    min_fc_fg = minimal_fourier_coefficient(f_conv_g, n + m)
    
    disc_f = max_plus_fourier_transform(f_coeffs, 2 ** n)[-1] - min_plus_fourier_transform(f_coeffs, 2 ** n)[0]
    disc_g = max_plus_fourier_transform(g_coeffs, 2 ** m)[-1] - min_plus_fourier_transform(g_coeffs, 2 ** m)[0]
    disc_fg = max_plus_fourier_transform(f_conv_g, 2 ** (n + m))[-1] - min_plus_fourier_transform(f_conv_g, 2 ** (n + m))[0]
    
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
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")