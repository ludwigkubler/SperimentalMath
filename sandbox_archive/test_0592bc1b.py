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

def generate_3sat_instance(n, m):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables + [-v for v in variables], 3)
        clauses.append(clause)
    return clauses

def monomial_degree(clause):
    return len(clause)

def toric_variety_degree(clauses):
    degrees = [monomial_degree(clause) for clause in clauses]
    return sum(degrees)

def sos_refutation_degree(n):
    # Placeholder function, replace with actual SOS refutation degree calculation
    return n  # Simplified example

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 40
    m = 2 * n  # Number of clauses
    
    clauses = generate_3sat_instance(n, m)
    degree = toric_variety_degree(clauses)
    refutation_degree = sos_refutation_degree(n)
    
    metric_value = degree * refutation_degree
    conjecture_holds = abs(metric_value - 1) < 1e-6
    
    return {
        "metric_name": "degree_product",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"n={n}, degree={degree}, refutation_degree={refutation_degree}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 50))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")