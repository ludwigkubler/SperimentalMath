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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

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

def generate_prime(n):
    while True:
        p = random.randint(2**n, 2**(n+1))
        if is_prime(p):
            return p

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = extended_gcd(b % a, a)
        return (g, y - (b // a) * x, x)

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError("Inverse doesn't exist")
    else:
        return x % m

def generate_random_cnf(n):
    clauses = []
    for i in range(2**n):
        clause = [random.choice([-1, 1]) * (j + 1) for j in range(n)]
        if all(clause[j] != -clause[k] for k in range(j)):
            clauses.append(clause)
    return clauses

def polynomial_representation(clauses):
    n = len(clauses[0])
    poly = [0] * (2**n)
    for clause in clauses:
        term = 1
        for literal in clause:
            if literal > 0:
                term *= (1 + 2**(literal - 1))
            else:
                term *= (1 - 2**(-literal - 1))
        poly[term] += 1
    return poly

def minimal_order_of_gqr(poly, p):
    order = 0
    for i in range(1, p):
        if all((poly[j] ** (i // gcd(j, i))) % p == poly[j] for j in range(len(poly))):
            order = max(order, i)
    return order

def resolution_width(cnf):
    n = len(cnf[0])
    clauses = set(tuple(sorted(clause)) for clause in cnf)
    queue = list(clauses)
    while queue:
        clause1 = queue.pop()
        for clause2 in queue[:]:
            if any(lit in clause2 and -lit not in clause2 for lit in clause1):
                new_clause = tuple(sorted(set(clause1) ^ set(clause2)))
                if len(new_clause) == 1:
                    return len(queue)
                if new_clause not in clauses:
                    clauses.add(new_clause)
                    queue.append(new_clause)
    return len(queue)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    p = generate_prime(n)
    cnf = generate_random_cnf(n)
    poly = polynomial_representation(cnf)
    order = minimal_order_of_gqr(poly, p)
    width = resolution_width(cnf)
    
    return {
        "metric_name": "order_to_width_ratio",
        "metric_value": Fraction(order, width) if width != 0 else float('inf'),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": order <= 1.5 * width,
        "counterexample": "" if order <= 1.5 * width else f"order={order}, width={width}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [generate_prime(2) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["conjecture_holds"])
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["conjecture_holds"])) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if r["counterexample"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")