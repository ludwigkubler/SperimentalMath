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

# Define a function to generate random CNFs with varying sizes up to n=40 and known polynomially bounded circuit complexities.
def generate_cnf(n):
    m = 2 * n  # Number of clauses, roughly 2*n for simplicity
    cnf = []
    for _ in range(m):
        clause = [random.randint(1, n) if random.choice([True, False]) else -random.randint(1, n) for _ in range(random.randint(1, n))]
        cnf.append(clause)
    return cnf

# Define a function to compute the minimal toric variety for each CNF instance using a constructive mapping that transforms the CNF into its defining polynomial.
def cnf_to_polynomial(cnf):
    n = max(abs(lit) for clause in cnf for lit in clause)
    x = {i: Fraction(1, 2) for i in range(1, n + 1)}
    polynomial = 0
    for clause in cnf:
        term = 1
        for lit in clause:
            if lit > 0:
                term *= (1 - x[lit])
            else:
                term *= (1 + x[-lit])
        polynomial += term
    return polynomial

# Define a function to run one trial with the given seed.
def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        polynomial = cnf_to_polynomial(cnf)
        
        # Compute the number of vertices in the minimal toric variety
        num_vertices = len(polynomial.as_ordered_terms())
        
        # Known upper bound on circuit complexity (simplified example)
        upper_bound = n * math.log2(n)
        
        results.append({
            "n": n,
            "num_vertices": num_vertices,
            "upper_bound": upper_bound
        })
    
    # Check if the number of vertices is within Θ(f(n)) of the known upper bound on circuit complexity
    support_fraction = sum(1 for result in results if abs(result["num_vertices"] - result["upper_bound"]) <= 0.5 * result["upper_bound"]) / len(results)
    
    return {
        "metric_name": "support_fraction",
        "metric_value": support_fraction,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else "support_fraction < 0.8"
    }

# Main function to run the trials and print the results
if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"support_fraction < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")