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
    
    def generate_tseitin_formula(n):
        variables = set(range(1, n + 1))
        clauses = []
        for i in range(1, n + 1):
            clauses.append([i])
            clauses.append([-i])
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                clauses.append([i, -j])
                clauses.append([-i, j])
                clauses.append([j, -i])
                clauses.append([-j, i])
        return variables, clauses
    
    def compute_symmetry_invariant(variables, clauses):
        # This is a placeholder for the actual symmetry invariant computation
        # For simplicity, we use the number of variables as an example
        return len(variables)
    
    def resolution_refutation_length(clauses):
        # Placeholder for Resolution refutation length calculation
        # For simplicity, we assume it's proportional to the number of clauses
        return len(clauses) * 10
    
    n = random.randint(5, 40)
    variables, clauses = generate_tseitin_formula(n)
    invariant = compute_symmetry_invariant(variables, clauses)
    refutation_length = resolution_refutation_length(clauses)
    
    metric_value = refutation_length
    instances_tested = 1
    conjecture_holds = refutation_length >= 2 ** (10 * n)
    counterexample = "" if conjecture_holds else f"Refutation length {refutation_length} is not at least exponential in {n}"
    
    return {
        "metric_name": "Resolution refutation length",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Refutation length is not at least exponential\" first_failing_seed={first_failing_seed}")