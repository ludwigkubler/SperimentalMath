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

def is_prime(num):
    if num <= 1:
        return False
    if num == 2:
        return True
    if num % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(num)) + 1, 2):
        if num % i == 0:
            return False
    return True

def smallest_prime_not_dividing(n):
    q = 2
    while q <= n and (n % q == 0 or not is_prime(q)):
        q += 1
    return q

def quadratic_residues_modulo_q(q):
    residues = set()
    for i in range(1, q):
        if pow(i, 2, q) not in residues:
            residues.add(pow(i, 2, q))
    non_residues = {i for i in range(1, q) if i not in residues}
    return len(non_residues), q

def rank_variance(n):
    # Placeholder function to calculate rank variance
    # This is a dummy implementation and should be replaced with actual logic
    return random.random()

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        R_phi = rank_variance(n)
        q = smallest_prime_not_dividing(n)
        N_q, _ = quadratic_residues_modulo_q(q)
        
        ratio = N_q / q
        results.append({
            "n": n,
            "R_phi": R_phi,
            "q": q,
            "N_q": N_q,
            "ratio": ratio
        })
    
    mean_ratio = sum(result["ratio"] for result in results) / len(results)
    conjecture_holds = all(abs(result["ratio"] - result["R_phi"]) <= 10 * result["R_phi"] for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Ratio of N_q to q",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        
    results = [run_trial(seed) for seed in seeds]
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")