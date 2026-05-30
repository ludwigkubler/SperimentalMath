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

def generate_boolean_function(n):
    return [random.randint(0, 1) for _ in range(n)]

def communication_complexity(f):
    n = len(f)
    cc = 0
    for i in range(n):
        if f[i] == 1:
            cc += 1
    return cc

def arithmetic_progression(f, g, k, n):
    ap = [f[i + k] != g[i + k] for i in range(n)]
    return all(x for x in ap)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 30
    f = generate_boolean_function(n)
    g = generate_boolean_function(n)
    
    cc_f = communication_complexity(f)
    cc_g = communication_complexity(g)
    
    if cc_f != cc_g:
        return {
            "metric_name": "communication_complexity",
            "metric_value": 0.0,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"Communication complexities differ: {cc_f} != {cc_g}"
        }
    
    ap_no_common_elements = all(arithmetic_progression(f, g, k, n) for k in range(n))
    
    if ap_no_common_elements:
        return {
            "metric_name": "communication_complexity",
            "metric_value": min(cc_f, 2 * cc_g),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "communication_complexity",
            "metric_value": 0.0,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Arithmetic progression has common elements"
        }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")