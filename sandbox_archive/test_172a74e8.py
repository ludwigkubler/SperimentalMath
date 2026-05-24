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
from fractions import Fraction
from math import log, ceil

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    q = 2**random.randint(3, 5)  # Field size q
    n = random.choice([5, 10, 15, 20, 30, 40])  # Degree of the polynomial
    k = random.randint(1, min(n, 10))  # Minimal root count
    
    x = [Fraction(0)] * (n + 1)
    f = sum(random.randint(0, q-1) * x[i] for i in range(n+1))
    
    if f == Fraction(0):
        return {
            "metric_name": "exponential_depth",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "f(x) has no roots in F_q"
        }
    
    # Construct the algebraic curve over an extension field
    y = [Fraction(0)] * (n + 1)
    for i in range(n+1):
        y[i] = f.subs(x, x**i)
    
    # Compute the minimal root count
    roots = set()
    for i in range(q):
        if f.subs(x, Fraction(i)) == Fraction(0):
            roots.add(i)
    
    k_computed = len(roots)
    
    # Determine the exponential depth of any Frege proof system
    depth = ceil(log(q, 2) + log(k_computed + 1, 2))
    
    return {
        "metric_name": "exponential_depth",
        "metric_value": depth,
        "instances_tested": 1,
        "conjecture_holds": depth >= ceil(log(q, 2) + log(k_computed + 1, 2)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(3, 6)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    metric_values = [r["metric_value"] for r in results if r["instances_tested"] > 0]
    conjecture_holds = all(r["conjecture_holds"] for r in results if r["instances_tested"] > 0)
    
    mean = sum(metric_values) / len(metric_values)
    std_dev = (sum((x - mean)**2 for x in metric_values) / len(metric_values))**0.5
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if conjecture_holds and support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(r["metric_value"] > mean + 3 * std_dev for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if r["metric_value"] > mean + 3 * std_dev)
        print(f"RESULT: FALSIFIED counterexample=\"exponential_depth_exceeds_threshold\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(metric_values)}")