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

def generate_random_boolean_function(n):
    return {i: random.randint(0, 1) for i in range(2**n)}

def evaluate_quadratic_form(f, x_k):
    n = int(math.log2(len(x_k)))
    Q = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        for j in range(i, n + 1):
            if i == j:
                Q[i][j] = f[(i << (n - 1)) | (j << (n - 2))]
            else:
                Q[i][j] = Q[j][i]
    return sum(Q[i][j] * x_k[i] * x_k[j] for i in range(n + 1) for j in range(i, n + 1))

def minimal_quadratic_defect(f):
    n = int(math.log2(len(f)))
    x_k_values = [list(range(2**n))]
    min_defect = float('inf')
    for x_k in x_k_values:
        defect = abs(evaluate_quadratic_form(f, x_k) - 1) / len(x_k)
        if defect < min_defect:
            min_defect = defect
    return min_defect

def communication_complexity(f):
    n = int(math.log2(len(f)))
    instances = [list(range(2**n)) for _ in range(30)]
    cc = 0
    for x_k in instances:
        cc += evaluate_quadratic_form(f, x_k)
    return cc / len(instances)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        f = generate_random_boolean_function(n)
        min_defect = minimal_quadratic_defect(f)
        cc = communication_complexity(f)
        if min_defect == 0 or cc == 0:
            continue
        results.append({
            "n": n,
            "min_defect": min_defect,
            "cc": cc,
            "ratio": abs(min_defect - cc) / cc
        })
    metric_value = sum(result["ratio"] for result in results) / len(results)
    instances_tested = len(results)
    n_max = max(result["n"] for result in results)
    conjecture_holds = all(math.isclose(result["ratio"], 1, rel_tol=0.1) for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "minimal_quadratic_defect_to_cc_ratio",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")