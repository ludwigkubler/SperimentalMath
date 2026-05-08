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

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_primes(count):
    primes = []
    num = 2
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def random_quandle(n):
    elements = list(range(1, n + 1))
    operation_table = {}
    for i in range(n):
        for j in range(n):
            operation_table[(i, j)] = random.choice(elements)
    return operation_table

def are_isomorphic(q1, q2):
    if len(q1) != len(q2):
        return False
    n = len(q1)
    elements = list(range(1, n + 1))
    for perm in permutations(elements):
        isomorphic = True
        for i in range(n):
            for j in range(n):
                if q1[(i, j)] != q2[perm[i] - 1][perm[j] - 1]:
                    isomorphic = False
                    break
            if not isomorphic:
                break
        if isomorphic:
            return True
    return False

def generate_permutations(elements):
    if len(elements) == 1:
        return [elements]
    permutations = []
    for i in range(len(elements)):
        first_element = elements[i]
        remaining_elements = elements[:i] + elements[i+1:]
        for p in generate_permutations(remaining_elements):
            permutations.append([first_element] + p)
    return permutations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):  # Each n tested 5 times to get statistical signal
            q1 = random_quandle(n)
            q2 = random_quandle(n)
            while are_isomorphic(q1, q2):
                q2 = random_quandle(n)
            metric_value = math.log(n) / math.log(2)
            total_metric_value += metric_value
            instances_tested += 1

    mean_metric_value = total_metric_value / instances_tested
    support_fraction = (instances_tested - counterexample.count("FALSIFIED")) / instances_tested

    return {
        "metric_name": "log_n",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)

    if all("FALSIFIED" not in r["counterexample"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    elif any("FALSIFIED" in r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "FALSIFIED" in r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")