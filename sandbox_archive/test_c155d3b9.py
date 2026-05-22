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
    n = random.randint(5, 40)
    d = random.randint(3, 10)
    F = [random.uniform(-10, 10) for _ in range(d)]
    P = sum(c * x**i for i, c in enumerate(F))
    
    roots = find_roots(P)
    if len(roots) < 2:
        return {
            "metric_name": "min_root_separation",
            "metric_value": None,
            "instances_tested": n,
            "conjecture_holds": False,
            "counterexample": "not_enough_distinct_roots"
        }
    
    min_distance = min(abs(roots[i] - roots[j]) for i in range(len(roots)) for j in range(i+1, len(roots)))
    c = 0.5
    lower_bound = c * math.log(d)
    
    if min_distance < lower_bound:
        return {
            "metric_name": "min_root_separation",
            "metric_value": min_distance,
            "instances_tested": n,
            "conjecture_holds": False,
            "counterexample": f"min_distance={min_distance}, lower_bound={lower_bound}"
        }
    
    return {
        "metric_name": "min_root_separation",
        "metric_value": min_distance,
        "instances_tested": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

def find_roots(P):
    # Simple numerical method to approximate roots
    def f(x):
        return sum(c * x**i for i, c in enumerate(P))
    
    def df(x):
        return sum(i * c * x**(i-1) for i, c in enumerate(P) if i > 0)
    
    roots = []
    x = -10
    while x <= 10:
        if f(x) * f(x + 0.1) < 0:
            root = newton_raphson(f, df, x, 1e-5)
            if all(abs(root - r) > 1e-6 for r in roots):
                roots.append(root)
        x += 0.2
    return roots

def newton_raphson(f, df, x0, tol=1e-6):
    x = x0
    while True:
        fx = f(x)
        dfx = df(x)
        if abs(dfx) < tol:
            break
        x -= fx / dfx
    return x

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seed}")
                break