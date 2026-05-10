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

def sturm_sequence(poly, deriv):
    seq = [poly]
    while deriv != [0]:
        seq.append([-deriv[0]/seq[-1][0]] + [b/a for a, b in zip(seq[-2], deriv[1:])])
        deriv = [b/a for a, b in zip(deriv[1:], deriv[2:])]
    return seq

def sturm_count(poly):
    seq = sturm_sequence(poly, poly_derivative(poly))
    count = 0
    sign_changes = lambda lst: sum(lst[i] * lst[i-1] < 0 for i in range(1, len(lst)))
    for a, b in zip(range(-100, 101), range(-100, 101)):
        count += sign_changes([f(a) for f in seq]) - sign_changes([f(b) for f in seq])
    return abs(count)

def poly_derivative(poly):
    return [i * coeff for i, coeff in enumerate(poly[1:], start=1)]

def generate_cnf(n):
    cnf = []
    for _ in range(n):
        clause = [random.choice([-1, 1]) * random.randint(1, n) for _ in range(random.randint(2, n))]
        cnf.append(clause)
    return cnf

def cnf_to_poly(cnf):
    poly = [1]
    for clause in cnf:
        term = [-1] + [0] * (max(abs(var) for var in clause))
        for var in clause:
            if var > 0:
                term[var] += 1
            else:
                term[-var] -= 1
        poly = [a * b for a, b in zip(poly, term)]
    return poly

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        poly = cnf_to_poly(cnf)
        root_count = sturm_count(poly)
        expected_root_count = round(2**(n/2))
        
        results.append({
            "n": n,
            "root_count": root_count,
            "expected_root_count": expected_root_count
        })
    
    total_instances_tested = len(results) * len(n_values)
    conjecture_holds = all(abs(result["root_count"] - result["expected_root_count"]) <= 5 for result in results)
    counterexample = "" if conjecture_holds else "n={n}, root_count={root_count}, expected_root_count={expected_root_count}"
    
    return {
        "metric_name": "real_root_count",
        "metric_value": sum(result["root_count"] for result in results) / total_instances_tested,
        "instances_tested": total_instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        primes = generate_primes(30)
        seeds = [p for p in primes if p <= 40]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['n']}, root_count={results[0]['root_count']}, expected_root_count={results[0]['expected_root_count']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")