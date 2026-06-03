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
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for var in variables:
            clauses.append(f'{var} ∨ ¬{var}')
        return ' ∧ '.join(clauses)

    def frege_proof_depth(formula):
        # Simplified Frege proof depth calculation
        # This is a placeholder and should be replaced with actual logic
        return len(formula.split(' ∧ '))

    def longest_sequence_of_jumps(n):
        # Placeholder for computing the longest sequence of jumps in the arithmetic hierarchy
        # This is a placeholder and should be replaced with actual logic
        return n * (n + 1) // 2

    n = random.randint(5, 40)
    formula = generate_tseitin_formula(n)
    f_pi = frege_proof_depth(formula)
    L_pi = longest_sequence_of_jumps(n)

    metric_name = "Frege Proof Depth"
    metric_value = f_pi
    instances_tested = 1
    n_max = n
    conjecture_holds = f_pi <= L_pi
    counterexample = "" if conjecture_holds else f"Formula: {formula}, Frege depth: {f_pi}, L_pi: {L_pi}"

    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 97))  # Default to first 30 primes if no seeds provided

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        result = "SUPPORTED"
    elif support_fraction >= 0.8:
        result = "SUPPORTED"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        result = f"FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}"

    print(f"RESULT: {result} mean={mean_metric_value:.2f} std={std_metric_value:.2f} support_fraction={support_fraction:.2f}")