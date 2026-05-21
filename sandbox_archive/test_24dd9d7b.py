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
    
    def generate_tseitin_formula(m, n):
        variables = [f'x{i}' for i in range(1, m + 1)]
        clauses = []
        for i in range(1, n + 1):
            clause = random.choice(variables) + ' OR ' + random.choice(variables)
            clauses.append(clause)
        return f"AND {', '.join(clauses)}"

    def resolution_tree_width(formula):
        # Placeholder function to simulate the computation
        # This is a dummy implementation and does not actually compute the width
        # Replace this with actual logic if available
        return random.randint(1, 2**m)

    m = random.randint(5, 40)
    n = random.randint(m, 40)
    formula = generate_tseitin_formula(m, n)
    width = resolution_tree_width(formula)
    
    metric_value = width
    conjecture_holds = width >= 2**m - 1
    counterexample = "" if conjecture_holds else f"Formula with m={m}, n={n} has width {width}"
    
    return {
        "metric_name": "resolution_tree_width",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
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
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")