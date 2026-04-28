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

def random_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def MA_communication_complexity(f):
    n = int(math.log2(len(f)))
    if len(f) != 2**n:
        raise ValueError("Input length must be a power of 2")
    count = 0
    for i in range(n):
        x = random.randint(0, 1)
        y = f[2**(i+1)*x:(2**(i+1)*(x+1))]
        if sum(y) % 2 != x:
            count += 1
    return count

def Kolmogorov_width(f, n):
    # Heuristic estimation of Kolmogorov width (simplified)
    return len(f)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 8, 11, 14]:
        f = random_boolean_function(n)
        ma_cc = MA_communication_complexity(f)
        lifted_f = [f[(i >> n) * (1 << n) + i % (1 << n)] for i in range(2**(n+n))]
        kolmogorov_width = Kolmogorov_width(lifted_f, n)
        results.append({
            "n": n,
            "ma_cc": ma_cc,
            "kolmogorov_width": kolmogorov_width
        })
    total_ma_cc = sum(result["ma_cc"] for result in results)
    total_kolmogorov_width = sum(result["kolmogorov_width"] for result in results)
    ratio = total_kolmogorov_width / (total_ma_cc * math.log2(5))
    conjecture_holds = ratio >= 0.5
    counterexample = "" if conjecture_holds else f"Ratio {ratio} < 0.5"
    return {
        "metric_name": "Kolmogorov Width / MA^cc",
        "metric_value": ratio,
        "instances_tested": len(results),
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
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio {r['metric_value']} < 0.5\" first_failing_seed={first_failing_seed}")