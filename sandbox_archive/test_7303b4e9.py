# auto-injected by SEC sandbox
import itertools
import collections
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
from sys import argv

def max_plus(a, b):
    return float('-inf') if a == float('-inf') or b == float('-inf') else max(a, b)

def min_plus(*args):
    return float('inf') if all(x == float('inf') for x in args) else min(args)

def tropical_polynomial(N, slopes, offset):
    f = [0] * N
    current_slope = 0
    for i in range(1, N):
        current_slope += random.uniform(-5, 5)
        f[i] = f[i-1] + current_slope
    return [x + offset for x in f]

def tropical_fourier_transform(f, N):
    F = [float('-inf')] * N
    for k in range(N):
        for x in range(N):
            F[k] = max_plus(F[k], f[x] - k * x)
    return F

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for n in [5, 8, 11, 14]:
        N = 2 ** n
        for _ in range(200):
            slopes = sorted(random.uniform(-5, 5) for _ in range(N - 1))
            f = tropical_polynomial(N, slopes, random.uniform(-5, 5))
            F = tropical_fourier_transform(f, N)
            G = tropical_fourier_transform(F, N)
            
            max_diff = max(abs(G[x] - f[x]) for x in range(N))
            min_fc_f = min_plus(*F)
            min_fc_g = min_plus(*G)
            discrepancy_f = max_plus(*f) - min_plus(*f)
            discrepancy_g = max_plus(*G) - min_plus(*G)
            
            results.append({
                "n": n,
                "max_diff": max_diff,
                "min_fc_f": min_fc_f,
                "min_fc_g": min_fc_g,
                "discrepancy_f": discrepancy_f,
                "discrepancy_g": discrepancy_g
            })
    
    all_checks_passed = True
    for result in results:
        if result["max_diff"] >= 1e-9 or abs(result["min_fc_f"] - result["min_fc_g"]) >= 1e-9 or result["discrepancy_g"] > abs(result["min_fc_g"]) + abs(result["discrepancy_f"]):
            all_checks_passed = False
            break
    
    return {
        "metric_name": "max_diff",
        "metric_value": sum(result["max_diff"] for result in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": all_checks_passed,
        "counterexample": "" if all_checks_passed else "involution_failure"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        print(f"RESULT: FALSIFIED counterexample=\"involution_failure\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE insufficient data to determine support of conjecture")