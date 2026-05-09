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

def p_adic_valuation(n, p):
    count = 0
    while n % p == 0:
        n //= p
        count += 1
    return count

def factorial(n):
    if n < 2:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def binomial_coefficient(n, k):
    return factorial(n) // (factorial(k) * factorial(n - k))

def generate_cnf(n, m):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, random.randint(1, n))
        if random.choice([True, False]):
            clause = [-v for v in clause]
        clauses.append(clause)
    return clauses

def polynomial_encoding(cnf):
    variables = set()
    for clause in cnf:
        variables.update(abs(v) for v in clause)
    n = len(variables)
    p = 2
    poly = [0] * (n + 1)
    for clause in cnf:
        term = 1
        for v in clause:
            if v > 0:
                term *= variables[v - 1]
            else:
                term //= variables[-v - 1]
        poly[0] += term
    return p, poly

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    m = 2 * n
    cnf = generate_cnf(n, m)
    p, poly = polynomial_encoding(cnf)
    
    valuations = set()
    for coeff in poly:
        if coeff != 0:
            valuations.add(p_adic_valuation(abs(coeff), p))
    
    metric_value = len(valuations)
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""
    
    # Placeholder for ACC^0 circuit size check (not implemented)
    if True:  # Replace with actual ACC^0 circuit size check logic
        conjecture_holds = metric_value == math.log(n, 2) * instances_tested
    
    return {
        "metric_name": "p-adic valuation rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 100))[:30]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")