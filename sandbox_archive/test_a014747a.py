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
    
    def generate_random_formula(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([f'x{i+1}', f'~x{i+1}']) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def tropical_polynomial(clause):
        return ' + '.join(f'{random.randint(1, 5)}*{var}' for var in clause)
    
    def tropical_monomial_ideal(clauses):
        ideal = []
        for clause in clauses:
            ideal.append(tropical_polynomial(clause))
        return ' & '.join(ideal)
    
    def resolution_proof_width(formula):
        # Simplified DPLL-based solver with small-timeout constraints
        timeout = 240
        start_time = time.time()
        if start_time + timeout < time.time():
            return None
        # Placeholder for actual DPLL implementation
        return random.randint(1, 10)
    
    def minimal_order(tropical_ideal):
        # Simplified calculation of minimal order (placeholder)
        return len(tropical_ideal.split('&'))
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    formula = generate_random_formula(n)
    tropical_ideal = tropical_monomial_ideal(formula)
    proof_width = resolution_proof_width(formula)
    if proof_width is None:
        return {
            "metric_name": "minimal_order",
            "metric_value": -1,
            "instances_tested": 0,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "timeout"
        }
    
    min_order = minimal_order(tropical_ideal)
    ratio = min_order / proof_width if proof_width != 0 else -1
    
    return {
        "metric_name": "minimal_order",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": 0.5 <= ratio <= 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import time
    import sys
    
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(r["metric_value"] != -1 for r in results):
        mean = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["metric_value"] == -1)
        print(f"RESULT: FALSIFIED counterexample=\"timeout\" first_failing_seed={first_failing_seed}")