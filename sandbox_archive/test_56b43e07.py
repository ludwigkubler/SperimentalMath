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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x

def matrix_multiply(A, B):
    m, k = len(A), len(B[0])
    n = len(B)
    C = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(n):
                C[i][j] += A[i][l] * B[l][j]
    return C

def spectral_radius(matrix):
    n = len(matrix)
    eigenvalues = [1.0]
    while len(eigenvalues) < n:
        v = [random.random() for _ in range(n)]
        v /= sum(v)
        v_next = matrix_multiply(matrix, v)
        v_next /= sum(v_next)
        lambda_new = sum(v[i] * v_next[i] for i in range(n))
        if abs(lambda_new - eigenvalues[-1]) < 1e-6:
            break
        eigenvalues.append(lambda_new)
    return max(eigenvalues)

def free_entropy(spectral_measure):
    return -sum(math.log(abs(z)) for z in spectral_measure) / len(spectral_measure)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    instances_tested = 30
    trivial_count = 0
    nontrivial_count = 0
    
    for _ in range(instances_tested):
        if random.random() < 0.5:
            # Trivial program: constant function
            transition_matrix = [[1] * n for _ in range(n)]
            spectral_measure = [n]
            lambda_P = 1
            phi_P = free_entropy(spectral_measure)
            trivial_count += 1
        else:
            # Nontrivial program: random read-twice branching program
            A = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
            B = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
            transition_matrix = matrix_multiply(A, B)
            eigenvalues = [complex(eigenvalue) for eigenvalue in spectral_radius(transition_matrix).real]
            lambda_P = max(abs(z.real) for z in eigenvalues)
            phi_P = free_entropy(eigenvalues)
            nontrivial_count += 1
        
        if phi_P < math.log(n):
            conjecture_holds = False
            counterexample = "phi_P < log(n)"
        elif phi_P >= n:
            conjecture_holds = True
            counterexample = ""
        else:
            conjecture_holds = False
            counterexample = "phi_P not in [log(n), n]"
        
        if lambda_P < 1 + 1 / n:
            conjecture_holds = False
            counterexample += ", lambda_P < 1 + 1/n"
        
        if phi_P >= n and lambda_P >= 1 + 1 / n:
            conjecture_holds = True
            counterexample = ""
        
        if not conjecture_holds:
            return {
                "metric_name": "phi_P",
                "metric_value": phi_P,
                "instances_tested": instances_tested,
                "conjecture_holds": False,
                "counterexample": counterexample
            }
    
    mean_phi_P = (trivial_count * math.log(n) + nontrivial_count * n) / instances_tested
    support_fraction = trivial_count / instances_tested
    
    return {
        "metric_name": "phi_P",
        "metric_value": mean_phi_P,
        "instances_tested": instances_tested,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']:.6f}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_phi_P = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_phi_P:.6f} std=NOT_COMPUTABLE support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"phi_P < log(n) or phi_P not in [log(n), n]\" first_failing_seed={first_failing_seed}")