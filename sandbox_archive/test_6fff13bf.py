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
    beta = 5
    n_values = [8, 12, 16, 20, 24, 28, 32, 36, 40]
    results = []
    
    for n in n_values:
        random.seed(seed * n)
        f_coeffs = [random.randint(0, 9) for _ in range(n)]
        
        def f(x):
            return sum(f_coeffs[i] * (x ** i) for i in range(n))
        
        def g(x):
            exp_sum = sum(math.exp((f(y) + f(x - y)) / beta) for y in range(n))
            return beta * math.log(exp_sum)
        
        def TFT_beta(h, k):
            exp_sum = sum(math.exp(h[x] / beta) * math.exp(-2 * math.pi * k * x / n) for x in range(n))
            return beta * math.log(abs(exp_sum))
        
        def MFC_beta(h):
            return min(TFT_beta(h, k) for k in range(1, n))
        
        MFC_f = MFC_beta(f)
        MFC_g = MFC_beta(g)
        Delta = abs(MFC_g - 2 * MFC_f)
        
        results.append({
            "n": n,
            "Delta": Delta,
            "MFC_f": MFC_f,
            "MFC_g": MFC_g
        })
    
    max_Delta_over_B = max(Delta / (3 * beta * math.log(n)) for n, Delta in zip(n_values, [result["Delta"] for result in results]))
    mean_Delta = sum(result["Delta"] for result in results) / len(results)
    
    return {
        "metric_name": "max_Delta_over_B",
        "metric_value": max_Delta_over_B,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": max_Delta_over_B <= 1.0,
        "counterexample": "" if max_Delta_over_B <= 1.0 else f"max_Delta_over_B = {max_Delta_over_B} > 1.0"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"max_Delta_over_B > 1.0\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")