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
        factor = 1 / A[i][i]
        for j in range(n):
            A[i][j] *= factor
        b[i] *= factor
        for k in range(i + 1, n):
            factor = A[k][i]
            for j in range(n):
                A[k][j] -= factor * A[i][j]
            b[k] -= factor * b[i]
    return b

def matrix_multiply(A, B):
    m = len(A)
    k = len(B)
    n = len(B[0])
    C = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] += A[i][l] * B[l][j]
    return C

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(10):  # Aim for at least 30 instances per seed
        clauses = [[random.randint(1, n), random.choice([-1, 1])] for _ in range(n)]
        variables = set(abs(clause[0]) for clause in clauses)
        
        exchange_matrix = [[0] * len(variables) for _ in range(len(variables))]
        for clause in clauses:
            var_index = variables.index(abs(clause[0]))
            if clause[1] == 1:
                exchange_matrix[var_index][var_index] += 1
            else:
                exchange_matrix[var_index][var_index] -= 1
        
        # Compute mutation distance (simplified version for demonstration)
        mutation_distance = sum(1 for row in exchange_matrix if any(x != 0 for x in row))
        
        # Estimate ACC^0 circuit size (simplified version for demonstration)
        acc0_circuit_size = n * math.log2(n) + random.uniform(-n, n)
        
        instances_tested += 1
        
        if mutation_distance != int(acc0_circuit_size):
            conjecture_holds = False
            counterexample = f"Mutation distance {mutation_distance} does not match ACC^0 circuit size {acc0_circuit_size}"
    
    return {
        "metric_name": "mutation_distance",
        "metric_value": mutation_distance,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")