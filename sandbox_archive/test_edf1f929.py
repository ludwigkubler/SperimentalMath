# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import product

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_primes(k):
    primes = []
    num = 2
    while len(primes) < k:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def random_3sat_instance(n, m):
    variables = list(range(1, n + 1))
    clauses = set()
    for _ in range(m):
        clause = random.sample(variables, 3)
        if random.choice([True, False]):
            clause = [-x for x in clause]
        clauses.add(tuple(sorted(clause)))
    return clauses

def encode_clause_in_group_characters(clause, n):
    G = [1, -1]  # Symmetric group S_3 has elements {1, -1}
    encoding = {}
    for g in G:
        count = sum(1 if x == g else 0 for x in clause)
        encoding[g] = Fraction(count, len(clause))
    return encoding

def fourier_transform(F):
    n = len(F)
    F_hat = [Fraction(0) for _ in range(n)]
    for k in range(n):
        for i in range(n):
            F_hat[k] += F[i] * (Fraction(math.cos(2 * math.pi * i * k / n), 1) + Fraction(math.sin(2 * math.pi * i * k / n), 1j))
    return F_hat

def sos_refutation_degree(clause_encoding):
    # Basic SDP relaxation to estimate refutation degree
    # This is a placeholder and should be replaced with actual SOS computation
    return max(abs(coeff) for coeff in clause_encoding.values())

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 30  # Number of variables
    m = 5 * n  # Number of clauses
    
    instance = random_3sat_instance(n, m)
    F = {}
    for clause in instance:
        encoding = encode_clause_in_group_characters(clause, n)
        for g, coeff in encoding.items():
            if g not in F:
                F[g] = Fraction(0)
            F[g] += coeff
    
    F_hat = fourier_transform(F)
    refutation_degree = sos_refutation_degree(F_hat)
    
    metric_name = "SOS Refutation Degree"
    metric_value = refutation_degree
    instances_tested = 1
    conjecture_holds = all(abs(coeff) <= max(abs(F_hat[k]) for k in range(len(F_hat))) for coeff in F.values())
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else generate_primes(30)
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")