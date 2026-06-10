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

def generate_random_boolean_function(n):
    return [random.randint(0, 1) for _ in range(2**n)]

def polynomial_from_boolean_function(f):
    n = int(math.log2(len(f)))
    poly = [[f[i]] + [0] * (n - 1) for i in range(len(f))]
    for j in range(n - 1):
        new_poly = []
        for k in range(2**n):
            if f[k] == 1:
                new_poly.append(poly[k][j+1])
            else:
                new_poly.append(poly[k][j])
        poly = new_poly
    return poly

def tropical_derivative(poly, n):
    derivative = [0] * (n + 1)
    for i in range(n + 1):
        if poly[i] == 1:
            derivative[i] = 1
    return derivative

def communication_complexity_rank_variance(f):
    n = int(math.log2(len(f)))
    circuit_ranks = []
    for k in range(1, n + 1):
        rank = 0
        for i in range(n - k + 1):
            subfunction = [f[i + j] for j in range(k)]
            if sum(subfunction) > rank:
                rank = sum(subfunction)
        circuit_ranks.append(rank)
    return sum((circuit_ranks[i] - sum(circuit_ranks) / len(circuit_ranks)) ** 2 for i in range(len(circuit_ranks))) / len(circuit_ranks)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    mt_values = []
    rc_values = []
    instances_tested = 0
    n_max = 0

    for n in n_values:
        f = generate_random_boolean_function(n)
        poly = polynomial_from_boolean_function(f)
        mt = tropical_derivative(poly, n)
        rc = communication_complexity_rank_variance(f)
        
        mt_values.append(mt)
        rc_values.append(rc)
        instances_tested += len(f)
        if n > n_max:
            n_max = n

    correlation_coefficient = sum((mt_values[i] - sum(mt_values) / len(mt_values)) * (rc_values[i] - sum(rc_values) / len(rc_values)) for i in range(len(mt_values))) / (len(mt_values) * math.sqrt(sum((mt_values[i] - sum(mt_values) / len(mt_values)) ** 2 for i in range(len(mt_values)))) * math.sqrt(sum((rc_values[i] - sum(rc_values) / len(rc_values)) ** 2 for i in range(len(rc_values)))))
    
    conjecture_holds = correlation_coefficient >= 0.9
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.9"

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.9\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data_or_unsupported")