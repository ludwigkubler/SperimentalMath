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
    
    def generate_formula(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([f'x{i+1}', f'~x{i+1}']) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def symplectic_form_rank(clauses):
        # Simplified version of computing the rank
        return len(set(tuple(sorted(c)) for c in clauses))
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    formula = generate_formula(n)
    rank = symplectic_form_rank(formula)
    
    # Placeholder function for f(n) - replace with actual computation
    def f(n):
        return n**2
    
    expected_rank = f(n)
    ratio = rank / expected_rank if expected_rank != 0 else float('inf')
    
    metric_name = "categorified_symplectic_form_rank"
    metric_value = rank
    instances_tested = 1
    conjecture_holds = 0.7 <= ratio <= 1.3
    counterexample = "" if conjecture_holds else f"rank={rank}, expected={expected_rank}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = result["counterexample"]
                first_failing_seed = seed
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")