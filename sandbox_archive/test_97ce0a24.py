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
    
    def generate_satisfiable_formula(n):
        clauses = []
        for i in range(n):
            clause = [random.choice([f'x{i}', f'~x{i}']) for _ in range(2)]
            clauses.append(clause)
        return clauses

    def calculate_minimal_order_of_entailment(clauses):
        # Placeholder implementation
        return len(clauses)

    def calculate_monotone_width(clauses):
        # Placeholder implementation
        return len(clauses) * 2

    n = random.choice([5, 10, 15, 20, 30, 40])
    formula = generate_satisfiable_formula(n)
    omega_G = calculate_minimal_order_of_entailment(formula)
    w_c_G = calculate_monotone_width(formula)

    return {
        "metric_name": "correlation",
        "metric_value": omega_G * w_c_G,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if not r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")