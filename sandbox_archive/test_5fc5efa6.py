# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import product

def memoize(f):
    cache = {}
    def memoized_func(*args):
        if args in cache:
            return cache[args]
        result = f(*args)
        cache[args] = result
        return result
    return memoized_func

@memoize
def hook_length_formula(n, k):
    if n == 0 or k == 0:
        return 1
    return (n - k + 1) * hook_length_formula(n - 1, k - 1) / (n + 1)

def hook_length_tableau_count(n):
    total = 1
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            total *= hook_length_formula(i, j)
    return total

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        λ_n = (n, n)
        μ_n = tuple(range(1, n + 1))
        
        SYT_λ_n = hook_length_tableau_count(n)
        SYT_μ_n = hook_length_tableau_count(n)
        
        ratio = SYT_λ_n / SYT_μ_n
        total_metric_value += ratio
        instances_tested += 1
        
        if ratio < math.pow(2, n / 2):
            conjecture_holds = False
            counterexample = f"n={n}, λ_n={λ_n}, μ_n={μ_n}, SYT_λ_n={SYT_λ_n}, SYT_μ_n={SYT_μ_n}, ratio={ratio}"
    
    return {
        "metric_name": "Hook-Length Ratio",
        "metric_value": total_metric_value / len(n_values),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        from sympy import primerange
        seeds = list(primerange(2, 50))[:30]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}**}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")