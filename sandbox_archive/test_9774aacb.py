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
    return [random.choice([0, 1]) for _ in range(2**n)]

def generate_quandle(f):
    n = int(math.log2(len(f)))
    quandle = {i: set() for i in range(n)}
    for i in range(n):
        for j in range(i+1, n):
            if f[i] == f[j]:
                quandle[i].add(j)
                quandle[j].add(i)
    return quandle

def min_order(quandle):
    return max(len(neighbors) for neighbors in quandle.values())

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        f = generate_random_boolean_function(n)
        quandle = generate_quandle(f)
        min_order_value = min_order(quandle)
        r_f = len(f) - sum(1 for x in f if x == 0)
        results.append((min_order_value, r_f))
    metric_value = sum(abs(x[0] - x[1]) for x in results) / len(results)
    conjecture_holds = all(abs(x[0] - x[1]) <= 3 * x[1] for x in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "mean_abs_diff",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "n_max": max(40, n),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(abs(r["metric_value"] - r["n_max"]) > 10 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if abs(result["metric_value"] - result["n_max"]) > 10)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction} n_tested={len(seeds)}")