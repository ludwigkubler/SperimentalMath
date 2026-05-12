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

def generate_sipser_function(n):
    def sipser(x):
        return sum(1 for i in range(n) if x[i] == 1 and (i + 1) % 2 == 0)
    return sipser

def generate_symmetric_group_representations(n):
    # Simplified representation using Young tableau characters
    representations = []
    for k in range(n + 1):
        rep = [math.comb(n, i) * math.comb(i, k) / math.factorial(k) for i in range(n)]
        representations.append(rep)
    return representations

def compute_fourier_coefficient(f, representation):
    n = len(representation)
    coeff = sum(f(tuple(range(n))) * representation[i] for i in range(n)) / n
    return abs(coeff)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    max_coefficients = []
    circuit_sizes = []

    for n in n_values:
        f = generate_sipser_function(n)
        representations = generate_symmetric_group_representations(n)
        max_coeff = 0
        for rep in representations:
            coeff = compute_fourier_coefficient(f, rep)
            if coeff > max_coeff:
                max_coeff = coeff

        # Simplified ACC⁰ circuit size (logarithm of n)
        circuit_size = math.log2(n)

        max_coefficients.append(max_coeff)
        circuit_sizes.append(circuit_size)

    log_coeffs = [math.log(coeff) for coeff in max_coefficients]
    log_sizes = [math.log(size) for size in circuit_sizes]

    # Linear regression to check inverse proportionality
    n_samples = len(log_coeffs)
    sum_log_coeffs = sum(log_coeffs)
    sum_log_sizes = sum(log_sizes)
    sum_log_coeffs_times_log_sizes = sum(a * b for a, b in zip(log_coeffs, log_sizes))
    sum_log_coeffs_squared = sum(coeff ** 2 for coeff in log_coeffs)

    slope = (n_samples * sum_log_coeffs_times_log_sizes - sum_log_coeffs * sum_log_sizes) / (n_samples * sum_log_coeffs_squared - sum_log_coeffs ** 2)
    intercept = (sum_log_coeffs - slope * sum_log_sizes) / n_samples

    r_squared = (n_samples * sum_log_coeffs_times_log_sizes - sum_log_coeffs * sum_log_sizes) ** 2 / ((n_samples * sum_log_coeffs_squared - sum_log_coeffs ** 2) * (n_samples * sum_log_sizes ** 2 - sum_log_sizes ** 2))

    conjecture_holds = r_squared > 0.8
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "r_squared",
        "metric_value": r_squared,
        "instances_tested": n_samples,
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
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")

    mean_r_squared = sum(result["metric_value"] for result in results) / len(results)
    std_r_squared = math.sqrt(sum((result["metric_value"] - mean_r_squared) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_r_squared} std={std_r_squared} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")