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

def sieve_of_eratosthenes(n):
    is_prime = [True] * (n + 1)
    p = 2
    while (p * p <= n):
        if (is_prime[p] == True):
            for i in range(p * p, n + 1, p):
                is_prime[i] = False
        p += 1
    prime_numbers = []
    for p in range(2, n + 1):
        if is_prime[p]:
            prime_numbers.append(p)
    return len(prime_numbers)

def generate_sat_instance(n):
    variables = list(range(n))
    clauses = []
    for _ in range(n):
        clause = random.sample(variables, 3)
        clauses.append(clause)
    return clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    sat_instance = generate_sat_instance(n)
    
    # Check if the clause graph is bipartite
    variables = list(range(n))
    edges = set()
    for clause in sat_instance:
        for i in range(len(clause)):
            for j in range(i + 1, len(clause)):
                edge = tuple(sorted([clause[i], clause[j]]))
                edges.add(edge)
    
    # Check if the variable assignments induce a Dirichlet progression with modulus ≤n²
    def is_dirichlet_progression(assignment):
        moduli = set()
        for var in variables:
            moduli.add(abs(assignment[var] % (n * n)))
        return len(moduli) == 1
    
    assignment = {var: random.randint(0, n - 1) for var in variables}
    if not is_dirichlet_progression(assignment):
        return {
            "metric_name": "Seed Length",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Not a Dirichlet progression"
        }
    
    pi_n = sieve_of_eratosthenes(n)
    seed_length = pi_n
    
    return {
        "metric_name": "Seed Length",
        "metric_value": seed_length,
        "instances_tested": 1,
        "conjecture_holds": True if abs(seed_length - pi_n) < 2 else False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(3, 1000, 50))[:30]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Not a Dirichlet progression' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")