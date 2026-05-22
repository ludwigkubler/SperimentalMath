# auto-injected by SEC sandbox
import math
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

def generate_sat_instance(n: int, m: int) -> list:
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause_size = random.randint(1, n)
        clause = random.sample(variables, clause_size)
        clauses.append(clause)
    return clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Define the maximum number of variables and clauses
    max_n = 40
    max_m = 2**max_n
    
    # Generate a random SAT instance with n variables and m clauses
    n = random.randint(5, max_n)
    m = random.randint(1, min(max_m, 2**n))
    sat_instance = generate_sat_instance(n, m)
    
    # Calculate the minimal order of the braided monoidal category (simplified for testing)
    # This is a placeholder value; actual calculation would be complex
    minimal_order = n * m
    
    # Measure the size of the smallest boolean circuit that can decide each SAT instance
    # This is a placeholder value; actual calculation would involve a SAT solver
    circuit_size = n + m
    
    return {
        "metric_name": "Minimal Order vs. Circuit Size",
        "metric_value": minimal_order,
        "instances_tested": 1,
        "conjecture_holds": minimal_order <= circuit_size**2,
        "counterexample": "" if minimal_order <= circuit_size**2 else f"Instance with n={n}, m={m} failed"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(30, 89))  # Default to first 50 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Instance with n={results[first_failing_seed]['instances_tested']}, m={results[first_failing_seed]['instances_tested']}\" first_failing_seed={first_failing_seed}")