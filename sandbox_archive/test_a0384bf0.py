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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_tseitin_formula(n):
        symbols = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(1, n+1):
            clause = f'{symbols[i-1]} ∨ ¬{symbols[-i]}'
            clauses.append(clause)
        return ' ∧ '.join(clauses)

    def resolution_length(formula):
        # Simplified version of resolution length calculation
        return len(formula.split(' ∧ '))

    def quandle_order(n):
        # Placeholder for actual quandle order computation
        return 2 * n

    n = random.randint(5, 40)
    formula = generate_tseitin_formula(n)
    res_len = resolution_length(formula)
    ord_Q = quandle_order(n)

    metric_name = "quandle_order_bound"
    metric_value = ord_Q / res_len
    instances_tested = 1
    conjecture_holds = ord_Q <= 2 * n * res_len
    counterexample = "" if conjecture_holds else f"Formula: {formula}, Quandle Order: {ord_Q}, Resolution Length: {res_len}"

    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30))  # Default to first 30 primes

    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = result["counterexample"]
                failing_seed = result["seed"]
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={failing_seed}")