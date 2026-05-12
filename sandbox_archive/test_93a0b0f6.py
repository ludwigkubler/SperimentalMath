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

def random_dnf(n, size_limit):
    terms = set()
    for _ in range(random.randint(1, min(size_limit, n**2))):
        term = tuple(sorted(random.sample(range(n), random.randint(1, n))))
        if term not in terms:
            terms.add(term)
    return terms

def max_matching_size(dnf):
    n = len(dnf[0])
    matching = set()
    for term in dnf:
        available_vars = set(range(n)) - {var for var in range(n) if any(var in t for t in matching)}
        for var in term:
            if var in available_vars:
                matching.add((var, term))
                break
    return len(matching)

def max_edge_packing(n):
    edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
    matching = set()
    for edge in edges:
        if all(edge[0] not in e and edge[1] not in e for e in matching):
            matching.add(edge)
    return len(matching)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        size_limit = n**2
        dnf = random_dnf(n, size_limit)
        mu_F = max_matching_size(dnf)
        if len(dnf) == n * (n - 1) // 2:  # k-CLIQUE instance
            mu_F = max_edge_packing(n)
        
        results.append({
            "n": n,
            "size_limit": size_limit,
            "dnf": dnf,
            "mu_F": mu_F
        })
    
    total_mu_F = sum(result["mu_F"] for result in results)
    mean_mu_F = total_mu_F / len(results)
    std_mu_F = math.sqrt(sum((result["mu_F"] - mean_mu_F) ** 2 for result in results) / len(results))
    
    conjecture_holds = all(mu_F <= math.log(n) or mu_F >= n**(1 - 1/n) for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "mu_F",
        "metric_value": mean_mu_F,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_mu_F = sum(result["metric_value"] for result in results)
    mean_mu_F = total_mu_F / len(results)
    std_mu_F = math.sqrt(sum((result["metric_value"] - mean_mu_F) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_mu_F} std={std_mu_F} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE mapping_undefined")