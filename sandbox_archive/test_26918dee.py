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

def log_sum_exp(x):
    max_x = max(x)
    return max_x + math.log(sum(math.exp(xi - max_x) for xi in x))

def maslov_dequantized_fourier_transform(h, beta):
    omega = cmath.exp(2j * math.pi / 8)
    n = len(h)
    mfc = float('inf')
    for k in range(n):
        if k == 0:
            continue
        sum_exp = log_sum_exp([beta * h[j] + 1j * omega**(k*j) for j in range(n)])
        mfc = min(mfc, abs(sum_exp))
    return -mfc / beta

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 8
    f = [random.uniform(0, 1) for _ in range(n)]
    g = [min(f[i] + f[j] for i in range(n) for j in range(n)) for k in range(n)]
    
    results = []
    for beta in [5, 10, 20, 50, 100, 200]:
        mfc_f = maslov_dequantized_fourier_transform(f, beta)
        mfc_g = maslov_dequantized_fourier_transform(g, beta)
        delta = abs(mfc_g - 2 * mfc_f)
        bound = 10 * math.log(8) / beta
        results.append((delta, bound))
    
    metric_name = "Delta"
    metric_value = sum(delta for delta, _ in results) / len(results)
    instances_tested = len(results)
    n_max = n
    conjecture_holds = all(delta <= bound for delta, bound in results)
    counterexample = "" if conjecture_holds else f"beta={results[0][1]}, delta={results[0][0]}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")