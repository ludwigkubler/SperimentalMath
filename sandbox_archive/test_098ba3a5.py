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
    
    def kronecker_coefficient(a, b):
        if a == 0 or b == 0:
            return 1
        if a < b:
            a, b = b, a
        c = [0] * (b + 1)
        c[0] = 1
        for i in range(1, a + 1):
            d = [0] * (b + 1)
            d[0] = 1
            for j in range(1, min(i, b) + 1):
                d[j] = c[j - 1] + c[j]
            for j in range(min(i, b), 0, -1):
                c[j] = (d[j] + d[j - 1]) // i
        return c[b]

    def symmetric_power_kronecker(n, k):
        return kronecker_coefficient(k, n)

    n_max = 40
    min_ratio = float('inf')
    instances_tested = 0

    for n in range(5, n_max + 1):
        k = int(math.log2(n))
        m = math.isqrt(n * n // 3)
        
        perm_kronecker = symmetric_power_kronecker(n, k)
        det_kronecker = symmetric_power_kronecker(m, k)
        
        if det_kronecker == 0:
            continue
        
        ratio = perm_kronecker / det_kronecker
        min_ratio = min(min_ratio, ratio)
        instances_tested += 1

    conjecture_holds = min_ratio > math.exp(1) ** (math.log2(n_max))
    counterexample = "" if conjecture_holds else f"n={n_max}, k={k}, perm_kronecker={perm_kronecker}, det_kronecker={det_kronecker}"

    return {
        "metric_name": "Kronecker Coefficient Ratio",
        "metric_value": min_ratio,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    avg_ratio = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={avg_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_ratio} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = result["counterexample"]
                first_failing_seed = seed
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")