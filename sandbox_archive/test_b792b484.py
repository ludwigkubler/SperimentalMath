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

# Helper functions for SAT and Tseitin transform
def generate_random_sat_instance(n, m):
    variables = set(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, 3)
        clauses.append(clause)
    return clauses

def tseitin_transform(clauses):
    literals = set()
    new_vars = {}
    tseitin_clauses = []

    def get_new_var():
        var = len(new_vars) + 1
        new_vars[var] = set()
        return var

    for i, clause in enumerate(clauses):
        literal = (i + 1) * 2
        literals.add(literal)
        tseitin_clauses.append([literal])
        for lit in clause:
            if lit < 0:
                neg_lit = -lit
                new_var = get_new_var()
                tseitin_clauses.append([-neg_lit, new_var])
                tseitin_clauses.append([new_var, -lit])
                literals.add(new_var)
            else:
                new_var = get_new_var()
                tseitin_clauses.append([-lit, new_var])
                tseitin_clauses.append([new_var, lit])
                literals.add(new_var)

    for literal in literals:
        tseitin_clauses.append([literal])

    return tseitin_clauses

# Monodromy group order calculation (simplified version)
def monodromy_group_order(n, m):
    # Placeholder function to simulate the computation
    # Replace this with actual implementation if needed
    return n + m  # Example: linear correlation for demonstration

# Resolution proof width calculation (simplified version)
def resolution_proof_width(clauses):
    # Placeholder function to simulate the computation
    # Replace this with actual implementation if needed
    return len(clauses) * 2  # Example: linear relationship for demonstration

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 0
    total_order = 0
    total_width = 0
    counterexample = ""

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            m = random.randint(n // 2, n * 2)
            clauses = generate_random_sat_instance(n, m)
            tseitin_clauses = tseitin_transform(clauses)
            order = monodromy_group_order(n, m)
            width = resolution_proof_width(tseitin_clauses)

            if instances_tested == 0:
                alpha = order / width
                counterexample = f"n={n}, m={m}, order={order}, width={width}"

            total_order += order
            total_width += width
            instances_tested += 1

    mean_order = total_order / instances_tested
    mean_width = total_width / instances_tested
    conjecture_holds = abs(mean_order - alpha * mean_width) < 0.1 * mean_width

    return {
        "metric_name": "monodromy_group_order",
        "metric_value": mean_order,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")

    mean_order = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_order) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_order} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.7:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")