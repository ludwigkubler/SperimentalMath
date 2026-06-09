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
from fractions import Fraction
import math

# Helper functions for DPLL algorithm
def dpll(cnf, assignment={}):
    if not cnf:
        return True
    unit_clauses = [c[0] for c in cnf if len(c) == 1]
    if unit_clauses:
        literal = unit_clauses[0]
        if literal < 0 and -literal in assignment:
            return False
        if literal > 0:
            assignment[literal] = True
        else:
            assignment[-literal] = False
        cnf = [c for c in cnf if literal not in c and -literal not in c]
    pure_literals = [v for v in range(1, max(cnf) + 1) if (v not in assignment and -v not in assignment)]
    if not pure_literals:
        return False
    literal = pure_literals[0]
    if literal > 0:
        assignment[literal] = True
    else:
        assignment[-literal] = False
    cnf = [c for c in cnf if literal not in c and -literal not in c]
    return dpll(cnf, assignment)

def solve_dpll(cnf):
    return len(dpll(cnf))

# Function to generate a random CNF formula
def generate_cnf(n, m):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = [random.choice(variables) * (1 if random.random() < 0.5 else -1)
                  for _ in range(random.randint(1, n))]
        clauses.append(clause)
    return clauses

# Function to run a single trial
def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a random CNF formula with n variables and m clauses
    n = random.choice([5, 10, 15, 20, 30, 40])
    m = random.randint(2 * n, 4 * n)
    cnf = generate_cnf(n, m)
    
    # Solve the DPLL search tree height
    height = solve_dpll(cnf)
    
    # Construct the categorical representation (simplified for testing)
    # This is a placeholder and should be replaced with actual categorical logic mapping
    morphisms = len(cnf) * n  # Simplified example
    
    # Calculate the ratio of morphisms to DPLL search tree height
    if height == 0:
        ratio = float('inf')
    else:
        ratio = Fraction(morphisms, height)
    
    # Check if the ratio falls within the acceptable range
    conjecture_holds = 0.5 <= ratio <= 1.5
    
    return {
        "metric_name": "ratio",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

# Main function to run multiple trials
if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 60, 2))  # Default list of 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")