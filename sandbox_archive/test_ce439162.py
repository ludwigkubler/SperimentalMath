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
    n_values = [8, 12, 16, 20, 24, 28, 32]
    results = []
    
    for n in n_values:
        deltas = []
        for _ in range(200):
            f = [random.uniform(0, 1) for _ in range(n)]
            g = min_plus_self_convolution(f, n)
            delta_value = delta(f, g, 5, n)
            deltas.append(delta_value)
        
        mean_delta = sum(deltas) / len(deltas)
        max_delta = max(deltas)
        R_n = max_delta / mean_delta
        bound = 3 + math.log2(n) / 4
        
        results.append({
            "n": n,
            "mean_delta": mean_delta,
            "max_delta": max_delta,
            "R_n": R_n,
            "bound": bound,
            "conjecture_holds": R_n <= bound
        })
    
    return {
        "metric_name": "R(n)",
        "metric_value": sum(result["R_n"] for result in results) / len(results),
        "instances_tested": 200 * len(n_values),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": all(result["conjecture_holds"] for result in results),
        "counterexample": "" if all(result["conjecture_holds"] for result in results) else f"First failing n: {min(n for n, result in enumerate(results) if not result['conjecture_holds'])}"
    }

def min_plus_self_convolution(f, n):
    g = [0] * n
    for i in range(n):
        for j in range(n):
            g[(i + j) % n] += f[i] + f[j]
    return g

def delta(f, g, beta, n):
    omega = math.exp(2j * math.pi / n)
    mfcb_f = maslov_dequantized_dft(f, beta, n)
    mfcb_g = maslov_dequantized_dft(g, beta, n)
    return abs(mfcb_g - 2 * mfcb_f)

def maslov_dequantized_dft(f, beta, n):
    omega = math.exp(2j * math.pi / n)
    sum_exp = 0
    for k in range(n):
        if k == 0:
            continue
        term = 1
        for x in range(n):
            term *= math.exp(-beta * f[x] * omega**(k*x))
        sum_exp += term
    return abs(sum_exp / n)

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")