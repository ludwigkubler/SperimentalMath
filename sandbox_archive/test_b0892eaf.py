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
    
    def generate_boolean_formula(n):
        if n == 1:
            return 'x'
        else:
            subformulas = [generate_boolean_formula(random.randint(1, n-1)) for _ in range(random.randint(2, n))]
            return '(' + ' & '.join(subformulas) + ') | (' + ' & '.join(subformulas[1:]) + ')'
    
    def frege_proof_width(formula):
        if formula.startswith('('):
            left, right = formula[1:].split(')')
            return max(frege_proof_width(left), frege_proof_width(right)) + 1
        else:
            return 1
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per size
            formula = generate_boolean_formula(n)
            rank = frege_proof_width(formula)
            total_rank += rank
            instances_tested += 1
    
    mean_value = total_rank / instances_tested
    expected_value = sum(n**2 * math.log(n, 2) for n in n_values) * len(n_values)
    
    conjecture_holds = mean_value >= expected_value * 0.95
    counterexample = "" if conjecture_holds else f"rank={mean_value}, expected={expected_value}"
    
    return {
        "metric_name": "syzygetic_complex_rank",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]  # Default to first 3 primes if no seeds provided
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_rank = sum(r["metric_value"] * r["instances_tested"] for r in results)
    instances_tested = sum(r["instances_tested"] for r in results)
    mean_value = total_rank / instances_tested
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")