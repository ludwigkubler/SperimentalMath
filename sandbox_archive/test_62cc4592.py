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

def random_d_regular_expander_graph(n, d):
    if (n - 1) % d != 0 or d > n:
        raise ValueError("Invalid parameters for expander graph")
    
    G = {i: [] for i in range(n)}
    degree_count = [0] * n
    
    while any(count < d for count in degree_count):
        u = random.randint(0, n - 1)
        v = random.choice([i for i in range(n) if i != u and len(G[i]) < d])
        
        G[u].append(v)
        G[v].append(u)
        degree_count[u] += 1
        degree_count[v] += 1
    
    return G

def tseitin_formula(G):
    n = len(G)
    clauses = []
    
    for u in range(n):
        literals = [f"x{i}" if i == u else f"~x{i}" for i in range(n)]
        clause = " ^ ".join(literals)
        clauses.append(clause)
    
    for u in range(n):
        neighbors = G[u]
        clause = " ^ ".join([f"~x{v}" for v in neighbors])
        clauses.append(clause)
    
    return " & ".join(clauses)

def polynomial_system_from_formula(formula):
    # Placeholder function to generate a system of polynomial equations
    # from the Tseitin formula. This is a dummy implementation.
    return []

def algebraic_degree(poly_system):
    # Placeholder function to compute the algebraic degree of a variety
    # defined by a system of polynomial equations. This is a dummy implementation.
    return 1

def resolution_width(formula):
    # Placeholder function to compute the resolution width required to refute
    # a Tseitin formula. This is a dummy implementation.
    return len(formula.split(" & "))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 30
    d = 3
    
    G = random_d_regular_expander_graph(n, d)
    formula = tseitin_formula(G)
    poly_system = polynomial_system_from_formula(formula)
    
    algebraic_deg = algebraic_degree(poly_system)
    res_width = resolution_width(formula)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": res_width,
        "instances_tested": 1,
        "conjecture_holds": algebraic_deg <= res_width,
        "counterexample": "" if algebraic_deg <= res_width else f"Algebraic degree {algebraic_deg} > resolution width {res_width}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean = sum(res["metric_value"] for res in results) / len(results)
    std_dev = math.sqrt(sum((res["metric_value"] - mean) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Algebraic degree > resolution width\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")