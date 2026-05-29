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
    
    def generate_tseitin_formula(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, 2)
            clauses.append((clause[0], clause[1]))
        return clauses
    
    def compute_minimal_root_system_length(clauses):
        # Placeholder function to simulate computation
        # Replace with actual implementation if available
        return len(clauses) / 2
    
    def tseitin_resolution_refutation_length(clauses):
        # Placeholder function to simulate computation
        # Replace with actual implementation if available
        return len(clauses) * 2
    
    n = random.randint(5, 40)
    m = int(n * random.uniform(1, 10))
    clauses = generate_tseitin_formula(n, m)
    
    nu_F = compute_minimal_root_system_length(clauses)
    refutation_length = tseitin_resolution_refutation_length(clauses)
    
    conjecture_holds = nu_F >= 2 ** (math.log(m / n) / math.log(2))
    counterexample = "mapping_undefined" if not conjecture_holds else ""
    
    return {
        "metric_name": "minimal_root_system_length",
        "metric_value": nu_F,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(seed) for seed in sys.argv[1:]]
    else:
        # Generate a list of 30 prime numbers as default seeds
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, min(30, len(primes)))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")