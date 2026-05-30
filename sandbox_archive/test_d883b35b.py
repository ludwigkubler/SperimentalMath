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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity(f):
        n = len(f)
        m = 2**n
        cc = 0
        for i in range(m):
            if f[i] == 1:
                cc += 1
        return cc
    
    def arithmetic_progression(f, g, k):
        n = len(f)
        return [f[(i + k) % n] for i in range(n)], [g[(i + k) % n] for i in range(n)]
    
    def has_common_elements(a, b):
        return any(x == y for x, y in zip(a, b))
    
    n = 10
    f = generate_boolean_function(n)
    g = generate_boolean_function(n)
    cc_f = communication_complexity(f)
    cc_g = communication_complexity(g)
    
    ap_no_common_elements = True
    for k in range(n):
        a, b = arithmetic_progression(f, g, k)
        if has_common_elements(a, b):
            ap_no_common_elements = False
            break
    
    conjecture_holds = cc_f <= 2 * cc_g if ap_no_common_elements else False
    counterexample = "mapping_undefined" if not ap_no_common_elements else ""
    
    return {
        "metric_name": "communication_complexity_ratio",
        "metric_value": cc_f / cc_g,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean = sum(r["metric_value"] for r in results) / len(results)
        std = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")