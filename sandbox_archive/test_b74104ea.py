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

def random_max_cut_instance(n):
    instance = [random.choice([0, 1]) for _ in range(n)]
    return instance

def monomials(n, degree):
    if degree == 0:
        return ["1"]
    result = []
    for i in range(n):
        for mono in monomials(n - i - 1, degree - 1):
            result.append(f"x{i}{mono}")
    return result

def gram_schmidt(monomials):
    n = len(monomials)
    Q = [[0] * n for _ in range(n)]
    R = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
    
    for k in range(n):
        norm = sum(Q[i][k]**2 for i in range(k, n))**0.5
        Q[k][k] = norm
        for i in range(k + 1, n):
            R[i][k] = sum(Q[j][k] * Q[j][i] for j in range(k, n))
            for j in range(k, n):
                Q[j][i] -= R[i][k] * Q[j][k]
    
    return Q, R

def moment_matrix(instance, degree):
    n = len(instance)
    monos = monomials(n, degree)
    m = len(monos)
    M = [[0] * m for _ in range(m)]
    
    for i in range(m):
        for j in range(i, m):
            count = 0
            for k in range(1 << n):
                if bin(k).count('1') == 2:
                    x_i = instance[k & 3]
                    x_j = instance[(k >> 2) & 3]
                    if (x_i + x_j) % 2 == 1:
                        count += 1
            M[i][j] = M[j][i] = count
    
    return M

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    degree = random.randint(2, 5)
    
    instance = random_max_cut_instance(n)
    M = moment_matrix(instance, degree)
    non_zero_entries = sum(sum(row) for row in M)
    
    threshold = n**2 / (degree**2)
    conjecture_holds = non_zero_entries >= threshold
    
    return {
        "metric_name": "non_zero_entries",
        "metric_value": non_zero_entries,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Instance with n={n}, degree={degree}"
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
    
    total_non_zero_entries = sum(res["metric_value"] for res in results)
    mean_non_zero_entries = total_non_zero_entries / len(results)
    std_non_zero_entries = (sum((res["metric_value"] - mean_non_zero_entries)**2 for res in results) / len(results))**0.5
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_non_zero_entries} std={std_non_zero_entries} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and support_fraction >= 0.8:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Instance with n={results[0]['instances_tested']}, degree=2\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction} < 80%")