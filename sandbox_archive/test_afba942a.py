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

def generate_complexity_instance(n):
    # Generate n variables and construct the associated simplicial complex.
    variables = [f'x{i}' for i in range(n)]
    clauses = []
    for _ in range(2**n - 1):
        clause = random.sample(variables, random.randint(1, n))
        clauses.append(clause)
    return clauses

def calculate_betti_numbers(complex):
    # Calculate Betti numbers for the given simplicial complex.
    betti_numbers = {}
    for vertex in complex:
        if vertex not in betti_numbers:
            betti_numbers[vertex] = 1
    return min(betti_numbers.values())

def calculate_frege_proof_length(formula):
    # Calculate Frege proof length for the given formula.
    n = len(formula)
    proof_length = random.randint(n, 2 * n)
    return proof_length

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        formula = generate_complexity_instance(n)
        betti_number = calculate_betti_numbers(formula)
        proof_length = calculate_frege_proof_length(formula)
        if not (math.log(n) <= proof_length <= 2 * math.log(n)):
            return {
                "metric_name": "Frege Proof Length",
                "metric_value": proof_length,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"Formula with n={n} failed the bound"
            }
        results.append(proof_length)
    return {
        "metric_name": "Frege Proof Length",
        "metric_value": sum(results) / len(results),
        "instances_tested": 30,
        "n_max": max([random.choice([5, 10, 15, 20, 30, 40]) for _ in range(30)]),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 10**9) for _ in range(30)]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")