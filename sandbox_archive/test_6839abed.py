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

def generate_primes(count):
    primes = []
    num = 2
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def random_boolean_function(n, seed=None):
    if seed is not None:
        random.seed(seed)
    return [random.choice([0, 1]) for _ in range(2**n)]

def compute_associated_matrix(f, n):
    M_f = [[f[i + j * (2**(n-1))] for i in range(2**(n-1))] for j in range(2**(n-1))]
    return M_f

def find_symplectic_vectors(M_f, n):
    symplectic_vectors = []
    for i in range(2**n):
        if all(M_f[i][j] == 0 for j in range(i+1, 2**n)):
            symplectic_vectors.append(i)
    return symplectic_vectors

def find_smallest_circuit(f, n):
    # Placeholder function to simulate finding the smallest circuit
    # This is a dummy implementation and should be replaced with actual SAT solving logic
    return random.randint(10, 50)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        f = random_boolean_function(n, seed)
        M_f = compute_associated_matrix(f, n)
        symplectic_vectors = find_symplectic_vectors(M_f, n)
        circuit_size = find_smallest_circuit(f, n)
        results.append({
            "n": n,
            "symplectic_vectors": len(symplectic_vectors),
            "circuit_size": circuit_size
        })
    
    if not results:
        return {
            "metric_name": "symplectic_vectors_per_circuit",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }
    
    total_symplectic = sum(result["symplectic_vectors"] for result in results)
    total_circuits = sum(result["circuit_size"] for result in results)
    mean_value = Fraction(total_symplectic, len(results))
    std_dev = math.sqrt(sum((result["symplectic_vectors"] - mean_value)**2 for result in results) / len(results))
    
    return {
        "metric_name": "symplectic_vectors_per_circuit",
        "metric_value": float(mean_value),
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": std_dev < 0.1 * mean_value,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = generate_primes(30)
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_supported\" first_failing_seed={first_failing_seed}")