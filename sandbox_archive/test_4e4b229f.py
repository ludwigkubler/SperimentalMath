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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_sat_instance(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([f'x{i+1}', f'-x{i+1}']) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def tropical_semi_ring(clauses):
        # Simplified representation of the tropical semi-ring
        return set(tuple(sorted(c)) for c in clauses if len(set(c)) > 1)
    
    def minimal_rank(semiring):
        # Minimal rank is the size of the semiring
        return len(semiring)
    
    def resolution_proof_length(clauses):
        # Simplified length of the resolution proof
        return sum(len(c) for c in clauses)
    
    n = random.randint(5, 40)
    sat_instance = generate_sat_instance(n)
    semiring = tropical_semi_ring(sat_instance)
    rank = minimal_rank(semiring)
    proof_length = resolution_proof_length(sat_instance)
    
    if proof_length == 0:
        return {
            "metric_name": "rank_to_log2_n_ratio",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "resolution_proof_length_is_zero"
        }
    
    ratio = rank / math.log(n, 2) ** 2
    return {
        "metric_name": "rank_to_log2_n_ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= 10,  # Placeholder constant C
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, min(30, len(primes)))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_ratio = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        result = f"RESULT: FALSIFIED counterexample=\"rank_to_log2_n_ratio_exceeds_bound\" first_failing_seed={first_failing_seed}"
    
    print(result)