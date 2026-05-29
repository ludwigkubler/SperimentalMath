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
    beta = 5
    n_values = [8, 12, 16, 20, 24, 28, 32, 36, 40]
    results = []
    
    random.seed(seed)
    for n in n_values:
        f = [random.randint(0, 9) for _ in range(n)]
        g = beta_softmax_self_convolution(f, beta, n)
        
        MFC_f = MFC_beta(f, beta, n)
        MFC_g = MFC_beta(g, beta, n)
        
        delta = abs(MFC_g - 2 * MFC_f)
        B_n = 3 * beta * math.log(n)
        
        results.append({
            "n": n,
            "delta": delta,
            "B_n": B_n
        })
    
    max_delta_over_B = max(result["delta"] / result["B_n"] for result in results)
    mean_delta = sum(result["delta"] for result in results) / len(results)
    std_delta = (sum((result["delta"] - mean_delta) ** 2 for result in results) / len(results)) ** 0.5
    
    conjecture_holds = max_delta_over_B <= 1.0
    counterexample = "" if conjecture_holds else "max_delta_over_B > 1"
    
    return {
        "metric_name": "delta_over_B",
        "metric_value": mean_delta,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def beta_softmax_self_convolution(f, beta, n):
    g = [0] * n
    for x in range(n):
        exp_sum = 0.0
        for y in range(n):
            exp_sum += math.exp((f[y] + f[(x - y) % n]) / beta)
        g[x] = beta * math.log(exp_sum)
    return g

def TFT_beta(h, k):
    n = len(h)
    exp_sum = 0.0
    for x in range(n):
        exp_sum += math.exp(h[x] / beta) * math.exp(-2 * math.pi * k * x / n)
    return beta * math.log(exp_sum)

def MFC_beta(h, beta, n):
    return min(TFT_beta(h, k) for k in range(1, n))

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_delta = sum(result["metric_value"] for result in results) / len(results)
    std_delta = (sum((result["metric_value"] - mean_delta) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_delta} std={std_delta} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"max_delta_over_B > 1\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=budget_exceeded n_tested={len(results)}")