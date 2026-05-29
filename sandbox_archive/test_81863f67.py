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

def binomial(n, k):
    if k > n:
        return 0
    if k == 0 or k == n:
        return 1
    k = min(k, n - k)
    c = 1
    for i in range(1, k + 1):
        c = c * (n - i + 1) // i
    return c

def forman_ricci_curvature(w_a, w_b, w_ab, denom):
    if denom == 0:
        return 0
    term1 = sum(w_a / math.sqrt(w_ab * w_f) for f in range(1, w_a))
    term2 = sum(w_b / math.sqrt(w_ab * w_f) for f in range(1, w_b))
    return w_a + w_b - term1 - term2

def estimate_mu(v, k):
    C_k_2 = binomial(k, 2)
    O_j = (1/2) * binomial(v, k) * C_k_2 * binomial(v-k, k-C_k_2)
    F_j = []
    for j in range(C_k_2 + 1):
        F_j.append(forman_ricci_curvature(j+1, j+1, j+1, 1))
    mu = sum(O_j[j] * F_j[j] for j in range(len(F_j))) / sum(O_j)
    return mu

def run_trial(seed: int) -> dict:
    random.seed(seed)
    v_values = [10, 16, 20, 24, 30, 40]
    results = []
    
    for v in v_values:
        k = math.ceil(math.log2(v))
        mu = estimate_mu(v, k)
        
        if mu < v / 4:
            continue
        
        gap = mu - v / 4
        n_max = k
        instances_tested = 1
        conjecture_holds = 0.05 * k <= gap <= 5 * k
        counterexample = "" if conjecture_holds else f"v={v}, gap={gap}"
        
        results.append({
            "metric_name": "saturation_gap",
            "metric_value": gap,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        })
    
    return {
        "seed": seed,
        "results": results
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    all_results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        all_results.extend(result["results"])
    
    mean_value = sum(r["metric_value"] for r in all_results) / len(all_results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in all_results) / len(all_results))
    support_fraction = sum(1 for r in all_results if r["conjecture_holds"]) / len(all_results)
    
    if all(r["conjecture_holds"] for r in all_results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in all_results):
        first_failing_seed = next(seed for seed, result in enumerate(all_results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")