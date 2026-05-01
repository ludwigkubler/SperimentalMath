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

def count_true_values(lst):
    return sum(lst)

def additive_energy(f):
    n = int(math.log2(len(f)))
    energy = 0
    for i in range(2**n):
        for j in range(i+1, 2**n):
            if f[i] == f[j]:
                energy += count_true_values([f[k] ^ f[l] for k in range(n) for l in range(k+1, n)])
    return energy

def correlation_with_linear_functions(f):
    n = int(math.log2(len(f)))
    max_corr = 0
    for a in range(2**n):
        corr = sum((f[i] ^ (a & (1 << i))) for i in range(n)) / len(f)
        if abs(corr) > max_corr:
            max_corr = abs(corr)
    return max_corr

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        f = generate_random_boolean_function(n)
        E_f = additive_energy(f)
        corr = correlation_with_linear_functions(f)
        instances_tested = len(n_values)
        conjecture_holds = False
        counterexample = ""
        if E_f >= n**(2 - 0.1):
            circuit_size_bound = n**(1 + 0.1)
            if corr < circuit_size_bound:
                conjecture_holds = True
            else:
                counterexample = "Counterexample found: high correlation with linear functions"
        results.append({
            "n": n,
            "E_f": E_f,
            "corr": corr,
            "circuit_size_bound": circuit_size_bound,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        })
    metric_value = sum(result["E_f"] for result in results) / instances_tested
    return {
        "metric_name": "Additive Energy",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": all(result["conjecture_holds"] for result in results),
        "counterexample": counterexample if any(result["counterexample"] for result in results) else ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = primes[:30]

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")

    results = [run_trial(seed) for seed in seeds]
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(result["counterexample"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")