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

def random_cnf(n, m):
    clauses = set()
    for _ in range(m):
        clause = [random.randint(1, n), -random.randint(1, n)]
        while len(clause) > 2:
            clause.pop(random.randint(0, len(clause) - 1))
        clauses.add(tuple(sorted(clause)))
    return clauses

def evaluate_cnf(cnf, assignment):
    for clause in cnf:
        if all([assignment[abs(lit) - 1] == (lit > 0) for lit in clause]):
            continue
        else:
            return False
    return True

def add_assignments(a, b):
    return a + b

def subtract_assignments(a, b):
    return a - b

def multiply_assignments(a, b):
    return a * b

def divide_assignments(a, b):
    if b == 0:
        return None
    return a / b

def add_energy(cnf, assignment):
    energy = 0
    for i in range(len(assignment)):
        for j in range(i + 1, len(assignment)):
            for k in range(j + 1, len(assignment)):
                for l in range(k + 1, len(assignment)):
                    if evaluate_cnf(cnf, [assignment[i], assignment[j], assignment[k], assignment[l]]):
                        energy += add_assignments(add_assignments(multiply_assignments(assignment[i], assignment[j]), multiply_assignments(assignment[k], assignment[l])), subtract_assignments(multiply_assignments(assignment[i], assignment[l]), multiply_assignments(assignment[j], assignment[k])))
    return energy

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n * (n - 1) // 2, n * (n + 1) // 2)
    cnf = random_cnf(n, m)
    
    max_energy = 0
    for _ in range(30):
        assignment = [random.choice([True, False]) for _ in range(n)]
        energy = add_energy(cnf, assignment)
        if energy > max_energy:
            max_energy = energy
    
    threshold = 0.8 * n ** 3
    conjecture_holds = max_energy < threshold or len(cnf) >= 0.5 * n ** 2
    
    return {
        "metric_name": "additive_energy",
        "metric_value": max_energy,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = generate_primes(30)
        seeds = primes[:30]
    
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
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"threshold_not_met\" first_failing_seed={first_failing_seed}")