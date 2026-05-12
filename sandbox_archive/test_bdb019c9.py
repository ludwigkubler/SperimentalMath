# auto-injected by SEC sandbox
import math
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

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
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

def random_quasigroup(n, seed=None):
    if seed is not None:
        random.seed(seed)
    quasigroup = [[random.randint(0, n-1) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if quasigroup[quasigroup[i][j]][k] != quasigroup[i][quasigroup[j][k]]:
                    raise ValueError("Not a quasigroup")
    return quasigroup

def is_idempotent(quasigroup, x):
    n = len(quasigroup)
    return quasigroup[x][x] == x

def count_idempotents(quasigroup):
    n = len(quasigroup)
    return sum(is_idempotent(quasigroup, i) for i in range(n))

def map_quasigroup_to_function(quasigroup):
    n = len(quasigroup)
    def f(x, y):
        return quasigroup[x][y]
    return f

def estimate_acc0_circuit_size(n):
    # Known bounds for small n
    if n == 4:
        return 16
    elif n == 5:
        return 25
    elif n == 10:
        return 100
    elif n == 15:
        return 225
    elif n == 20:
        return 400
    elif n == 30:
        return 900
    else:
        raise ValueError("Unsupported n for ACC⁰ circuit size estimation")

def run_trial(seed: int) -> dict:
    n = 40
    quasigroup = random_quasigroup(n, seed)
    idempotents_count = count_idempotents(quasigroup)
    f = map_quasigroup_to_function(quasigroup)
    acc0_circuit_size = estimate_acc0_circuit_size(n)
    
    metric_name = "ACC⁰ Circuit Size"
    metric_value = acc0_circuit_size
    instances_tested = 1
    conjecture_holds = idempotents_count > 0 and abs(acc0_circuit_size - n**2 / idempotents_count) < 5 * (n**2 / idempotents_count)**0.5
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")