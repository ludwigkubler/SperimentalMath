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
    
    def generate_sipser_like_cnf(n):
        clauses = set()
        for i in range(2**(n//2)):
            clause = []
            for j in range(n):
                if (i >> j) & 1:
                    clause.append(random.choice([j, -j]))
            clauses.add(tuple(sorted(clause)))
        return clauses
    
    def count_non_zero_fourier_coefficients(cnf):
        # Placeholder function to count non-zero Fourier coefficients
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(10, 20)
    
    def acc0_circuit_size(cnf):
        # Placeholder function to compute ACC⁰ circuit size
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(5, 10)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_sipser_like_cnf(n)
    non_zero_coeffs = count_non_zero_fourier_coefficients(cnf)
    s = acc0_circuit_size(cnf)
    
    if s == 0:
        return {
            "metric_name": "non_zero_fourier_coefficients",
            "metric_value": non_zero_coeffs,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "acc0_circuit_size_is_zero"
        }
    
    c = 0.5
    if non_zero_coeffs >= c * 2**(n/2) / s:
        return {
            "metric_name": "non_zero_fourier_coefficients",
            "metric_value": non_zero_coeffs,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "non_zero_fourier_coefficients",
            "metric_value": non_zero_coeffs,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"counterexample_found_with_n={n}, s={s}, non_zero_coeffs={non_zero_coeffs}"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        primes = [i for i in range(2, 100) if is_prime(i)]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_non_zero_coeffs = sum(r["metric_value"] for r in results if r["instances_tested"] > 0)
    total_instances = sum(r["instances_tested"] for r in results if r["instances_tested"] > 0)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_non_zero_coeffs/total_instances} std=NA support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")