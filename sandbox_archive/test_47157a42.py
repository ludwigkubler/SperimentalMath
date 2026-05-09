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
    return a * b // gcd(a, b)

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_primes(limit):
    primes = []
    for num in range(2, limit):
        if is_prime(num):
            primes.append(num)
    return primes

def generate_random_dnf(n, m):
    clauses = []
    for _ in range(m):
        clause = set()
        while len(clause) < 1 or len(clause) > n:
            clause = {random.randint(1, n) for _ in range(random.randint(1, n))}
        clauses.append(clause)
    return clauses

def rank_dnf(clauses, A):
    disjoint_clauses = []
    for clause in clauses:
        if not (clause & A):
            disjoint_clauses.append(clause)
    return len(disjoint_clauses)

def mu(dnf, k):
    n = len(dnf[0])
    max_rank_diff = 0
    for i in range(1 << n):
        A = {j+1 for j in range(n) if (i & (1 << j))}
        if len(A) <= k:
            rank_diff = rank_dnf(dnf, A) - len(A)
            if rank_diff > max_rank_diff:
                max_rank_diff = rank_diff
    return max_rank_diff

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n**2 // 10, n**2)
    dnf = generate_random_dnf(n, m)
    
    mu_value = mu(dnf, n)
    if mu_value > 2 * math.log(n):
        return {
            "metric_name": "mu(Φ)/log n",
            "metric_value": mu_value / math.log(n),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "general_dnf"
        }
    
    k = random.randint(2, 5)
    clique_dnf = generate_random_dnf(k, n)
    mu_clique_value = mu(clique_dnf, k-1)
    if mu_clique_value < n**0.5 / 2:
        return {
            "metric_name": "mu(k-CLIQUE)/n^{1/2}",
            "metric_value": mu_clique_value / (n**0.5),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"k-CLIQUE with k={k}"
        }
    
    return {
        "metric_name": "mu(Φ)/log n",
        "metric_value": mu_value / math.log(n),
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = generate_primes(100)
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}**}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")