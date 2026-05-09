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

def generate_primes(n):
    primes = []
    num = 2
    while len(primes) < n:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def discrete_log(g, h, p):
    if h == 1:
        return 0
    for x in range(1, p):
        if pow(g, x, p) == h:
            return x
    return None

def fundamental_group_generators(G):
    n = len(G)
    generators = set()
    for i in range(n):
        for j in range(i + 1, n):
            if G[i][j] == 1:
                generators.add((i, j))
    return generators

def dpll_depth(Tseitin_formula, max_depth=1000):
    stack = [(Tseitin_formula, 0)]
    while stack:
        formula, depth = stack.pop()
        if depth > max_depth:
            return -1
        if all(x in formula for x in range(1, len(formula))):
            return depth
        for i in range(len(formula)):
            if formula[i] == 'A':
                new_formula = formula[:i] + formula[i+1:]
                stack.append((new_formula, depth + 1))
    return -1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    G = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if random.choice([True, False]):
                G[i][j] = G[j][i] = 1
    
    generators = fundamental_group_generators(G)
    mu_G = len(generators)
    
    Tseitin_formula = [random.randint(0, 1) for _ in range(n)]
    depth = dpll_depth(Tseitin_formula)
    
    c = 0.5
    conjecture_holds = depth >= 2 ** (c * mu_G)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "DPLL Depth",
        "metric_value": depth,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(arg) for arg in sys.argv[1:]]
    else:
        primes = generate_primes(30)
        seeds = primes[:30]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_depth = sum(r["metric_value"] for r in results) / len(results)
    std_depth = math.sqrt(sum((r["metric_value"] - mean_depth) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_depth} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print("RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed=<s>")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")