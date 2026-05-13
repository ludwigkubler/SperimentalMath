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
from itertools import combinations_with_replacement, permutations

def partitions(k, n):
    if k == 0:
        yield []
    elif n == 0:
        yield [0] * k
    else:
        for p in partitions(k-1, n):
            yield [p[0]+1] + p[1:]
        for p in partitions(k, n-1):
            yield [p[0]] + p[1:]

def hook_length_formulas(n, k):
    if n == 0 and k == 0:
        return 1
    elif n == 0 or k == 0:
        return 0
    else:
        hook = (n+k-1) * (k+n-k) // 2
        return hook_length_formulas(n-1, k-1) + hook_length_formulas(n-1, k)

def plethysm_coefficient(n, k):
    perm = hook_length_formulas(n, k)
    det = hook_length_formulas(n, n-k)
    return perm / det

def generate_3sat_formula(n, m):
    variables = list(range(1, n+1))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, 3)
        clauses.append(clause)
    return clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        m = random.randint(2*n, 3*n)
        formula = generate_3sat_formula(n, m)
        lambda_diag = [len(list(g)) for _, g in itertools.groupby(sorted(formula), key=lambda x: len(x))]
        
        perm_coeff = plethysm_coefficient(n, n)
        det_coeff = plethysm_coefficient(n, 0)
        
        if perm_coeff <= det_coeff:
            conjecture_holds = False
            counterexample = f"n={n}, m={m}, lambda_diag={lambda_diag}"
            break
        
        total_metric_value += perm_coeff / det_coeff
        instances_tested += 1

    return {
        "metric_name": "plethysm_coefficient_gap",
        "metric_value": total_metric_value / instances_tested,
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

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")