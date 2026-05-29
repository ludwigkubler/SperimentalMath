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
    return abs(a * b) // gcd(a, b)

def factorial(n):
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def binomial_coefficient(n, k):
    if k > n:
        return 0
    if k == 0 or k == n:
        return 1
    k = min(k, n - k)
    numerator = factorial(n)
    denominator = factorial(k) * factorial(n - k)
    return numerator // denominator

def generate_monomial_ideal(n, m):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, random.randint(1, n))
        clauses.append(clause)
    return clauses

def is_valid_clique(G, clique):
    for u in clique:
        for v in clique:
            if u != v and (u, v) not in G or (v, u) not in G:
                return False
    return True

def find_max_clique(G):
    n = len(G)
    max_clique_size = 0
    max_clique = []
    for k in range(n, 0, -1):
        for clique in itertools.combinations(range(n), k):
            if is_valid_clique(G, clique) and len(clique) > max_clique_size:
                max_clique = list(clique)
                max_clique_size = len(clique)
    return max_clique

def generate_coxeter_group_action(G, I):
    n = len(G)
    orbits = set()
    for i in range(n):
        orbit = {tuple(sorted([G[i][j] for j in I]))}
        orbits.add(orbit)
    return orbits

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    m = 10
    I = generate_monomial_ideal(n, m)
    G = {i: [j for j in range(n) if i != j] for i in range(n)}
    
    orbits = generate_coxeter_group_action(G, I)
    num_orbits = len(orbits)
    complexity = m
    bound = math.ceil(complexity ** 1.5)
    
    metric_name = "Number of Orbits"
    metric_value = num_orbits
    instances_tested = 1
    conjecture_holds = num_orbits <= bound
    counterexample = "" if conjecture_holds else f"Expected {bound} orbits, got {num_orbits}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]]
    if not seeds:
        seeds = [2**i + 3**j + 5**k for i in range(5) for j in range(5) for k in range(5)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_orbits = sum(r["metric_value"] for r in results)
    num_trials = len(results)
    mean_orbits = total_orbits / num_trials
    std_orbits = math.sqrt(sum((r["metric_value"] - mean_orbits) ** 2 for r in results) / num_trials)
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / num_trials
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_orbits} std={std_orbits} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")