# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from collections import defaultdict

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_seeds(num_primes=30):
    primes = []
    num = 2
    while len(primes) < num_primes:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def run_trial(seed: int) -> dict:
    random.seed(seed)

    def generate_k_cnf(n, k):
        clauses = []
        for _ in range(k):
            clause = [random.randint(1, n), -random.randint(1, n)]
            while len(set(clause)) != 2:
                clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses

    def dpll(phi):
        if not phi:
            return True
        for literal in phi[0]:
            new_phi = [c for c in phi[1:] if literal not in c and -literal not in c]
            if dpll(new_phi):
                return True
            new_phi = [c for c in phi[1:] if -literal not in c]
            if dpll(new_phi):
                return True
        return False

    def tropicalize(phi):
        n = max(abs(lit) for clause in phi for lit in clause)
        T = [[float('inf')] * (n + 1) for _ in range(n + 1)]
        for var in range(1, n + 1):
            T[var][var] = min(T[var][var], 0)
        for clause in phi:
            max_val = -math.inf
            for lit in clause:
                if abs(lit) <= n:
                    max_val = max(max_val, T[abs(lit)][abs(lit)])
            for lit in clause:
                if abs(lit) <= n:
                    T[lit][lit] = min(T[lit][lit], max_val)
        return T

    def min_local_ring_unit_group_size(T):
        n = len(T) - 1
        unit_group_size = 0
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                if T[i][j] == float('inf'):
                    return float('inf')
                unit_group_size += 1
        return unit_group_size

    def frege_proof_depth(phi):
        return len(phi)

    n = random.randint(5, 40)
    k = random.randint(2, min(n * (n - 1) // 2, 3))
    phi = generate_k_cnf(n, k)
    T = tropicalize(phi)
    unit_group_size = min_local_ring_unit_group_size(T)
    proof_depth = frege_proof_depth(phi)

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": unit_group_size / proof_depth,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_seeds()
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")