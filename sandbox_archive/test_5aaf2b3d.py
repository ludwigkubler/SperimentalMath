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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def tropical_polynomial(n):
        return [random.uniform(0, 1) for _ in range(n)]
    
    def min_plus_convolution(f, g):
        n = len(f)
        result = [float('inf')] * n
        for i in range(n):
            for j in range(n):
                result[i] = min(result[i], f[i] + g[j - (i - j) % n])
        return result
    
    def maslov_dequantized_dft(h, beta, n):
        omega = math.exp(2j * math.pi / n)
        mfc = [0] * n
        for k in range(n):
            if k == 0:
                continue
            sum_exp = 0
            for x in range(n):
                sum_exp += math.exp(-beta * h[x]) * omega**(k * x)
            mfc[k] = abs(sum_exp) / n
        return min(mfc[1:])
    
    def delta(f, g, beta, n):
        mfcb_f = maslov_dequantized_dft(f, beta, n)
        mfcb_g = maslov_dequantized_dft(g, beta, n)
        return abs(mfcb_g - 2 * mfcb_f)
    
    beta = 5
    instances_tested = 0
    max_n = 0
    total_delta = 0.0
    max_delta = 0.0
    
    for n in [8, 12, 16, 20, 24, 28, 32]:
        if instances_tested >= 200:
            break
        
        for _ in range(200):
            f = tropical_polynomial(n)
            g = min_plus_convolution(f, f)
            delta_value = delta(f, g, beta, n)
            total_delta += delta_value
            max_delta = max(max_delta, delta_value)
            instances_tested += 1
            max_n = max(max_n, n)
    
    mean_delta = total_delta / instances_tested
    R_n = max_delta / mean_delta
    
    conjecture_holds = R_n <= (3 + math.log2(n) / 4 for n in [8, 12, 16, 20, 24, 28, 32])
    counterexample = "" if conjecture_holds else f"R({max_n})={R_n} > {3 + math.log2(max_n) / 4}"
    
    return {
        "metric_name": "R(n)",
        "metric_value": R_n,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_R_n = sum(r["metric_value"] for r in results) / len(results)
    std_R_n = math.sqrt(sum((r["metric_value"] - mean_R_n)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_R_n} std={std_R_n} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")