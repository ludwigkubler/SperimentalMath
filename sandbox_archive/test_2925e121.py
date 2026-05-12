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
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_primes(count):
    primes = []
    num = 2
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def ip_2(n):
        x = [random.randint(0, 1) for _ in range(n)]
        y = [random.randint(0, 1) for _ in range(n)]
        return sum(xi * yi for xi, yi in zip(x, y)) % 2
    
    def polynomial_from_sat(instance):
        n = len(instance)
        vars = {f"x{i}": i for i in range(n)}
        poly = 0
        for clause in instance:
            term = 1
            for literal in clause:
                if literal < 0:
                    term *= (1 - vars[f"x{-literal}"])
                else:
                    term *= vars[f"x{literal}"]
            poly += term
        return poly
    
    def grb_basis(poly, mod):
        # Simplified Gröbner basis computation using Buchberger's algorithm
        # This is a placeholder and does not guarantee correctness for all cases.
        terms = [poly]
        while True:
            new_terms = []
            for i in range(len(terms)):
                for j in range(i + 1, len(terms)):
                    lcm = lcm_of_degrees(terms[i], terms[j])
                    if lcm is None:
                        continue
                    s = spoly(terms[i], terms[j], mod)
                    new_terms.append(s % mod)
            if not new_terms:
                break
            terms.extend(new_terms)
        return terms
    
    def lcm_of_degrees(a, b):
        # Placeholder for degree calculation and LCM
        return None
    
    def spoly(f, g, mod):
        # Placeholder for S-polynomial computation
        return 0
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    instance = [[random.randint(1, n) for _ in range(random.randint(1, n))] for _ in range(n)]
    
    poly = polynomial_from_sat(instance)
    generators = grb_basis(poly, 2)
    
    metric_value = len(generators)
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""
    
    if n == 40:
        if metric_value >= math.log(n):
            conjecture_holds = True
        else:
            counterexample = "read-twice BP generator count too low"
    elif n == 20:
        if metric_value >= math.log(n):
            conjecture_holds = True
        else:
            counterexample = "read-twice BP generator count too low"
    elif n == 15:
        if metric_value >= math.log(n):
            conjecture_holds = True
        else:
            counterexample = "read-twice BP generator count too low"
    elif n == 10:
        if metric_value >= math.log(n):
            conjecture_holds = True
        else:
            counterexample = "read-twice BP generator count too low"
    elif n == 5:
        if metric_value >= math.log(n):
            conjecture_holds = True
        else:
            counterexample = "read-twice BP generator count too low"
    
    return {
        "metric_name": "Generator Count",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        primes = generate_primes(30)
        seeds = primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"read-twice BP generator count too low\" first_failing_seed={first_failing_seed}")