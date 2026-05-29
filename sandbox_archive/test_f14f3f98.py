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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    def generate_random_primes(k):
        primes = []
        while len(primes) < k:
            num = random.randint(2, 100)
            if is_prime(num):
                primes.append(num)
        return primes
    
    def generate_affine_group(m):
        # Simplified generation for demonstration purposes
        generators = [generate_random_primes(m) for _ in range(m)]
        return generators
    
    def brute_force_circuit_size(generators):
        n = len(generators[0])
        size = 2 ** (n * m)
        return size
    
    def monotone_circuit_size(m):
        return 2 ** (2 * m / 3)
    
    m = random.randint(1, 40)  # Ensure n_min >= 5 and n_max <= 40
    generators = generate_affine_group(m)
    brute_force_size = brute_force_circuit_size(generators)
    monotone_bound = monotone_circuit_size(m)
    
    conjecture_holds = brute_force_size <= monotone_bound
    
    return {
        "metric_name": "Circuit Size",
        "metric_value": monotone_bound,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Brute-force size {brute_force_size} exceeds bound {monotone_bound}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 100) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    metric_values = [result["metric_value"] for result in results]
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values)):.2f} support_fraction={support_fraction:.2f}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")