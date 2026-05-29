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
    random.seed(seed)
    
    def generate_polynomial(n):
        return [random.random() for _ in range(n)]
    
    def min_plus_convolution(f, g, n):
        result = [0] * n
        for i in range(n):
            for j in range(n):
                result[i] = max(result[i], f[j] + g[(i - j) % n])
        return result
    
    def maslov_dft(h, beta, n):
        omega = math.exp(2j * math.pi / n)
        sum_exp = 0
        for x in range(n):
            sum_exp += h[x] * math.exp(-beta * h[x]) * (omega ** (x * 5))
        return abs(sum_exp) / n
    
    def delta(f, g, beta, n):
        mfc_f = maslov_dft(f, beta, n)
        mfc_g = maslov_dft(g, beta, n)
        return abs(mfc_g - 2 * mfc_f)
    
    n_values = [8, 12, 16, 20, 24, 28, 32]
    results = []
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        deltas = []
        for _ in range(200):
            f = generate_polynomial(n)
            g = min_plus_convolution(f, f, n)
            delta_value = delta(f, g, 5, n)
            deltas.append(delta_value)
            instances_tested += 1
            n_max = max(n_max, n)
        
        mean_delta = sum(deltas) / len(deltas)
        max_delta = max(deltas)
        R_n = max_delta / mean_delta
        
        results.append({
            "n": n,
            "mean_delta": mean_delta,
            "max_delta": max_delta,
            "R_n": R_n
        })
    
    metric_name = "R(n)"
    metric_value = sum(result["R_n"] for result in results) / len(results)
    conjecture_holds = all(result["R_n"] <= 3 + math.log2(result["n"]) / 4 for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
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
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")