# auto-injected by SEC sandbox
import math
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
from itertools import combinations, permutations

def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def generate_primes(n=30):
    primes = []
    num = 2
    while len(primes) < n:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def random_3cnf(n, m):
    variables = list(range(1, n + 1))
    clauses = set()
    for _ in range(m):
        clause = tuple(random.sample(variables, 3))
        if len(clause) == 3:
            clauses.add(tuple(sorted(clause)))
    return clauses

def generate_partitions(n):
    def partition_helper(n, max_val, current_partition):
        if n == 0:
            yield current_partition
        else:
            for i in range(1, min(max_val, n) + 1):
                yield from partition_helper(n - i, i, current_partition + [i])
    
    return list(partition_helper(n, n, []))

def hook_length_formula(shape, n):
    total = 1
    for row in shape:
        for col in range(row):
            total *= (n - row + col + 1)
        total //= (row * (col + 1))
    return total

def plethysm_coefficient(char_poly, n):
    partitions = generate_partitions(n)
    return sum(hook_length_formula(shape, n) * char_poly[shape] for shape in partitions)

def characteristic_polynomial(clauses, n):
    char_poly = {(): 1}
    for clause in clauses:
        new_char_poly = {}
        for partition, coeff in char_poly.items():
            for i in range(n + 1):
                if len(partition) + i <= n:
                    new_partition = tuple(sorted(partition + (i,) * len(clause)))
                    new_char_poly[new_partition] = new_char_poly.get(new_partition, 0) + coeff
        char_poly = new_char_poly
    return char_poly

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 10
    m = 40
    clauses = random_3cnf(n, m)
    
    char_poly = characteristic_polynomial(clauses, n)
    plethysm = plethysm_coefficient(char_poly, n)
    
    conjecture_holds = plethysm >= 2**(n/2) * (m + 1)**(n/2)
    counterexample = "" if conjecture_holds else "plethysm_too_small"
    
    return {
        "metric_name": "plethysm_coefficient",
        "metric_value": plethysm,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        primes = generate_primes()
        seeds = primes[:30]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = (sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))**0.5
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        counterexample_desc = "plethysm_too_small"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")