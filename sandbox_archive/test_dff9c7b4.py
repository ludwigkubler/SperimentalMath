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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    g, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return g, x, y

def inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError("Modular inverse does not exist")
    else:
        return x % m

def binomial_coefficient(n, k):
    if k > n:
        return 0
    num = math.factorial(n)
    den = math.factorial(k) * math.factorial(n - k)
    return num // den

def generate_random_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = [random.randint(1, n), random.randint(-n, -1)]
        cnf.append(clause)
    return cnf

def incidence_polytope(cnf):
    n = len(cnf[0])
    polytope = [[0] * (2**n) for _ in range(n + 1)]
    polytope[0][0] = 1
    for clause in cnf:
        new_polytope = [[0] * (2**n) for _ in range(n + 1)]
        for i in range(2**n):
            if any(abs(i & (1 << abs(lit))) == 0 for lit in clause):
                continue
            for j in range(n + 1):
                new_polytope[j][i] += polytope[j - 1][i]
        polytope = new_polytope
    return polytope

def minimal_ehrhart_quotient(polytope):
    n = len(polytope) - 1
    volume = 0
    for i in range(2**n):
        if all(polytope[j][i] % (j + 1) == 0 for j in range(n)):
            volume += polytope[n][i]
    return volume / math.factorial(n)

def circuit_monotone_width(cnf):
    n = len(cnf[0])
    width = 0
    for i in range(2**n):
        stack = []
        for lit in cnf:
            if any(abs(i & (1 << abs(lit))) == 0 for lit in lit):
                continue
            if stack and stack[-1] == -lit:
                stack.pop()
            else:
                stack.append(lit)
        width = max(width, len(stack))
    return width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        cnf = generate_random_cnf(n, n * (n - 1))
        polytope = incidence_polytope(cnf)
        mu = minimal_ehrhart_quotient(polytope)
        w_m = circuit_monotone_width(cnf)
        results.append({"mu": mu, "w_m": w_m})
    if len(results) < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    mu_values = [result["mu"] for result in results]
    w_m_values = [result["w_m"] for result in results]
    correlation_coefficient = sum((x - mean_x) * (y - mean_y) for x, y in zip(mu_values, w_m_values)) / (len(results) * std_dev_x * std_dev_y)
    mu_squared_le_w_m = all(mu**2 <= w_m for mu, w_m in zip(mu_values, w_m_values))
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.5 and mu_squared_le_w_m,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient<0.5 or mu^2>w_m\" first_failing_seed={first_failing_seed}")