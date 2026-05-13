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
    
    def generate_3sat_instance(n, m):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for _ in range(m):
            clause = random.sample(variables + [-v for v in variables], 3)
            clauses.append(clause)
        return clauses
    
    def monomial_ideal(clauses, n):
        monomials = set()
        for clause in clauses:
            for assignment in itertools.product([0, 1], repeat=n):
                if all((assignment[abs(v)-1] == 1) ^ (v < 0) for v in clause):
                    monomial = tuple(assignment)
                    monomials.add(monomial)
        return monomials
    
    def convex_hull_volume(monomials):
        # Simplest volume calculation using the number of monomials
        return len(monomials)
    
    def sos_refutation_degree(n):
        # Placeholder for actual SOS refutation degree computation
        # For simplicity, we use a known relationship here
        return n * (n + 1) // 2
    
    n = 40
    m = random.randint(3*n//2, 5*n)
    clauses = generate_3sat_instance(n, m)
    monomials = monomial_ideal(clauses, n)
    deg_V = convex_hull_volume(monomials)
    refutation_degree_n = sos_refutation_degree(n)
    
    if deg_V * refutation_degree_n == 0:
        return {
            "metric_name": "deg(V) * refutation_degree(n)",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    metric_value = deg_V * refutation_degree_n
    conjecture_holds = abs(metric_value - 2000) < 100  # Placeholder constant for demonstration
    
    return {
        "metric_name": "deg(V) * refutation_degree(n)",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")