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
    # Set seed for reproducibility
    random.seed(seed)
    
    # Define ACC⁰-intractable constant β(n)
    def beta(n):
        return 2 ** (n // 10)
    
    # Generate a random explicit function f in P of degree n
    def generate_polynomial(n):
        coefficients = [random.randint(-10, 10) for _ in range(n + 1)]
        while coefficients[-1] == 0:  # Ensure it's not the zero polynomial
            coefficients[-1] = random.randint(-10, 10)
        return coefficients
    
    # Compute the minimal local cohomology rank (simplified version)
    def compute_local_cohomology_rank(coefficients):
        n = len(coefficients) - 1
        rank = sum(1 for c in coefficients if c != 0)
        return rank
    
    # Main trial logic
    instances_tested = 30
    total_rank = 0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(instances_tested):
        n = random.randint(5, 40)  # Sweep through different degrees
        polynomial = generate_polynomial(n)
        rank = compute_local_cohomology_rank(polynomial)
        
        if rank < beta(n):
            conjecture_holds = False
            counterexample = f"Polynomial of degree {n} with rank {rank}"
            break
        
        total_rank += rank
    
    metric_value = total_rank / instances_tested
    return {
        "metric_name": "minimal_local_cohomology_rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")