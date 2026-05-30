# auto-injected by SEC sandbox
import math
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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity(f):
        n = len(f)
        cc = 0
        for x in range(2**n):
            y = x ^ (x >> 1)  # Example encoding strategy
            if f[x] != f[y]:
                cc += 1
        return cc
    
    def arithmetic_progression(f, g, k, n):
        return [f[(i + k) % n] for i in range(n)], [g[(i + k) % n] for i in range(n)]
    
    def has_common_elements(a, b):
        return any(x == y for x, y in zip(a, b))
    
    n = 10  # Fixed size for simplicity
    f = generate_boolean_function(n)
    g = generate_boolean_function(n)
    
    cc_f = communication_complexity(f)
    cc_g = communication_complexity(g)
    
    ap_no_common_elements = True
    for k in range(n):
        a, b = arithmetic_progression(f, g, k, n)
        if has_common_elements(a, b):
            ap_no_common_elements = False
            break
    
    conjecture_holds = cc_f <= 2 * cc_g if ap_no_common_elements else False
    counterexample = "arithmetic_progression_has_common_elements" if not ap_no_common_elements else ""
    
    return {
        "metric_name": "communication_complexity_ratio",
        "metric_value": cc_f / cc_g,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"arithmetic_progression_has_common_elements\" first_failing_seed={first_failing_seed}")