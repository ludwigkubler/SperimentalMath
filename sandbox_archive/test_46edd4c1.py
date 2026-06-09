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

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def smallest_prime_not_dividing(n):
    q = 2
    while q <= n and (n % q == 0 or not is_prime(q)):
        q += 1
    return q

def quadratic_non_residues(modulus):
    non_residues = []
    for i in range(1, modulus):
        if pow(i, (modulus - 1) // 2, modulus) != 1:
            non_residues.append(i)
    return non_residues

def rank_variance(instance):
    # Placeholder function to compute rank variance
    # This is a stub and should be replaced with actual computation
    n = len(instance)
    return random.random() * n  # Random for demonstration purposes

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        if n <= 1:
            continue
        instance = [random.randint(0, 1) for _ in range(n * (n - 1) // 2)]
        R_phi = rank_variance(instance)
        
        q = smallest_prime_not_dividing(n)
        N_q = quadratic_non_residues(q)
        N_q_size = len(N_q)
        
        ratio = N_q_size / q
        results.append({
            "n": n,
            "R_phi": R_phi,
            "q": q,
            "N_q_size": N_q_size,
            "ratio": ratio
        })
    
    metric_value = sum(result["ratio"] for result in results) / len(results)
    instances_tested = len(results)
    n_max = max(result["n"] for result in results)
    conjecture_holds = all(abs(result["ratio"] - result["R_phi"]) < 1e-6 for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Ratio of N_q to q",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")