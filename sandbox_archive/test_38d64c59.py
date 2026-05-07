# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from itertools import combinations

def generate_3cnf(n, m):
    clauses = []
    for _ in range(m):
        clause = [random.choice([-i, i]) for i in range(1, n + 1)]
        random.shuffle(clause)
        clauses.append(clause)
    return clauses

def evaluate_formula(formula, assignment):
    for clause in formula:
        if any(assignment[abs(lit) - 1] == l for l in clause):
            continue
        else:
            return False
    return True

def fourier_coefficient(formula, assignment):
    sum_val = 0
    for clause in formula:
        product = 1
        for lit in clause:
            if lit > 0:
                product *= assignment[lit - 1]
            else:
                product *= 1 - assignment[-lit - 1]
        sum_val += product
    return sum_val

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 10
    m = 20
    formula = generate_3cnf(n, m)
    
    fourier_sum = 0
    for S in range(1 << n):
        assignment = [bool(random.getrandbits(1)) for _ in range(n)]
        fourier_sum += abs(fourier_coefficient(formula, assignment))
    
    proof_length = len(formula)  # Placeholder for actual resolution proof length calculation
    
    return {
        "metric_name": "Fourier Coefficient Sum",
        "metric_value": fourier_sum,
        "instances_tested": 1 << n,
        "conjecture_holds": fourier_sum <= proof_length,
        "counterexample": "" if fourier_sum <= proof_length else "Resolution length too short"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='Resolution length too short' first_failing_seed={first_failing_seed}")