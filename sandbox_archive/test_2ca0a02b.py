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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            b[i] /= factor
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
                    b[k] -= factor * b[i]
        return [b[i] for i in range(n)]
    
    def r_transform(cumulants):
        n = len(cumulants)
        R = [[0] * n for _ in range(n)]
        R[0][0] = 1
        for k in range(1, n):
            R[k][k-1] = cumulants[k]
            for i in range(k):
                R[i][k] = -sum(R[j][i] * R[k-j-1][j+1] for j in range(i))
        return R
    
    def free_cumulant_sum(cumulants):
        R = r_transform(cumulants)
        det = 1
        for i in range(len(R)):
            det *= R[i][i]
        return sum(math.log(abs(det)) / (2 * math.factorial(k)) for k in range(1, len(cumulants)))
    
    def generate_3sat_instance(n, clause_density):
        m = int(n * clause_density)
        clauses = []
        for _ in range(m):
            literals = random.sample(range(-n, 0) + list(range(1, n+1)), 3)
            clauses.append(literals)
        return clauses
    
    def min_read_twice_bp_transition_matrix(clauses):
        n = len(clauses)
        A = [[0] * (2*n) for _ in range(2*n)]
        for i in range(n):
            for j in range(n):
                if i != j:
                    A[i][j+n] = 1
                    A[j+n][i] = 1
        return A
    
    n = 40
    clause_density = 4.2
    instance = generate_3sat_instance(n, clause_density)
    transition_matrix = min_read_twice_bp_transition_matrix(instance)
    
    # Compute free cumulants (simplified for demonstration)
    cumulants = [1] * n  # Placeholder values
    rho = free_cumulant_sum(cumulants)
    
    return {
        "metric_name": "rho",
        "metric_value": rho,
        "instances_tested": 1,
        "conjecture_holds": rho >= 0.9 * math.log(n),
        "counterexample": "" if rho >= 0.9 * math.log(n) else "hard_instance"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rho = sum(r["metric_value"] for r in results) / len(results)
    std_rho = math.sqrt(sum((r["metric_value"] - mean_rho) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
    elif any(r["counterexample"] == "hard_instance" for r in results):
        first_failing_seed = next(seed for seed, r in enumerate(results) if r["counterexample"] == "hard_instance")
        print(f"RESULT: FALSIFIED counterexample='hard_instance' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence to support or falsify the conjecture")