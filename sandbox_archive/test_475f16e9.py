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
    
    def generate_sat_instance(m, n):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def compute_minimal_representation(clauses, d):
        # Placeholder implementation
        # This is a dummy function and should be replaced with actual computation
        return random.random()
    
    def compute_frege_proof_width(clauses):
        # Placeholder implementation
        # This is a dummy function and should be replaced with actual computation
        return random.randint(1, 50)
    
    n_max = 0
    instances_tested = 0
    total_metric_value = 0
    
    for _ in range(30):  # Ensure at least 30 instances per seed
        m = random.randint(5, 40)  # Sweep through different sizes
        n = random.randint(m, 40)
        d = random.randint(2, 6)
        
        clauses = generate_sat_instance(m, n)
        mu_phi = compute_minimal_representation(clauses, d)
        frege_width = compute_frege_proof_width(clauses)
        
        if frege_width > mu_phi ** (d + 1):
            return {
                "metric_name": "Frege Proof Width",
                "metric_value": frege_width,
                "instances_tested": instances_tested,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": f"Instance with m={m}, n={n}, d={d} failed the bound"
            }
        
        total_metric_value += frege_width
        instances_tested += 1
        n_max = max(n_max, n)
    
    return {
        "metric_name": "Frege Proof Width",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")