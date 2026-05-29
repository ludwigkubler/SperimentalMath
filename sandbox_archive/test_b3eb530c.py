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

def maslov_dequantized_fourier_transform(h, beta):
    n = len(h)
    omega = math.exp(2j * math.pi / n)
    tft_h = [0] * n
    for k in range(n):
        if k == 0:
            sum_exp = sum(math.exp(-beta * h[j]) for j in range(n))
        else:
            sum_exp = sum(math.exp(-beta * h[j]) * omega**(j*k) for j in range(n))
        tft_h[k] = -(1 / beta) * math.log(sum_exp)
    return tft_h

def min_plus_self_convolution(f):
    n = len(f)
    g = [float('inf')] * n
    for i in range(n):
        for j in range(n):
            k = (i + j) % n
            g[k] = min(g[k], f[i] + f[j])
    return g

def run_trial(seed: int) -> dict:
    random.seed(seed)
    beta_values = [5, 10, 20, 50, 100, 200]
    results = []
    
    for beta in beta_values:
        f = [random.uniform(0, 1) for _ in range(8)]
        g = min_plus_self_convolution(f)
        
        tft_f = maslov_dequantized_fourier_transform(f, beta)
        mfc_f = min(tft_f[k] for k in range(1, len(tft_f)))
        
        tft_g = maslov_dequantized_fourier_transform(g, beta)
        mfc_g = min(tft_g[k] for k in range(1, len(tft_g)))
        
        delta = abs(mfc_g - 2 * mfc_f)
        bound = 10 * math.log(8) / beta
        results.append((delta, bound))
    
    metric_value = sum(delta for delta, _ in results) / len(results)
    max_delta = max(delta for delta, _ in results)
    pass_rate = sum(1 for delta, _ in results if delta <= 0.5 * max_delta) / len(results)
    conjecture_holds = all(delta <= bound for delta, bound in results)
    
    return {
        "metric_name": "Delta",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "n_max": 8,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Δ={max_delta} > B(β) for β=200"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")