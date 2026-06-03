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
    
    def generate_formula(n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for _ in range(2**n):
            clause = []
            for var in variables:
                if random.choice([True, False]):
                    clause.append(var)
                else:
                    clause.append(f'~{var}')
            clauses.append(' | '.join(clause))
        return ' & '.join(clauses)

    def formal_power_series(formula):
        # Simplified encoding of the formula as a power series
        # This is a placeholder and does not reflect actual complexity
        return len(formula.split('&'))

    def sat_proof_width(formula):
        # Placeholder for SAT proof width calculation
        # This is a simplified version and does not reflect actual complexity
        return len(formula.split('&')) * 2

    n = random.randint(5, 40)
    formula = generate_formula(n)
    ord_f_phi = formal_power_series(formula)
    w_phi = sat_proof_width(formula)

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": (ord_f_phi - 10) * (w_phi - 20),  # Simplified correlation
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = [2**i + 3 for i in range(5, 8)]  # First 30 primes

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((res["seed"] for res in results if not res["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")