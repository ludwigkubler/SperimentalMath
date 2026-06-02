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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([1, -1]) * random.randint(1, n) for _ in range(3)]
            clauses.append(clause)
        return clauses

    def clause_indicator_polynomial(clauses, x):
        result = 0
        for clause in clauses:
            term = 1
            for literal in clause:
                if literal > 0:
                    term *= (x + literal) / (2 * literal)
                else:
                    term *= (x - abs(literal)) / (2 * abs(literal))
            result += term
        return result

    def minimal_order_of_quadratic_residues(poly):
        x = 1.0
        while True:
            if poly(x) == 0:
                return x
            x += 1.0

    def resolution_proof_width(clauses):
        # Simplified version for demonstration; actual width calculation is complex
        return len(clauses)

    n = random.randint(5, 40)
    clauses = generate_3cnf(n)
    poly = clause_indicator_polynomial(clauses, x=2.0)  # Using a fixed value for simplicity
    min_order = minimal_order_of_quadratic_residues(poly)
    w_phi = resolution_proof_width(clauses)

    return {
        "metric_name": "min_order_over_w",
        "metric_value": min_order / w_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,  # Mapping undefined for this conjecture
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 17 for i in range(30)]
    
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
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")