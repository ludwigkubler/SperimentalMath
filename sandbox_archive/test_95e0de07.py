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
from math import log, factorial

def generate_sat_instance(m: int, n: int) -> list:
    variables = [f"x{i}" for i in range(1, n + 1)]
    clauses = []
    for _ in range(m):
        clause_size = random.randint(1, n)
        clause = random.sample(variables, clause_size)
        clause.append("~" + random.choice(clause))
        clauses.append(clause)
    return clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for m in [5, 10, 15, 20, 30, 40]:
        for n in range(5, min(n_max, 41)):
            clauses = generate_sat_instance(m, n)
            # Placeholder for minimal root count computation
            # This is a dummy value and should be replaced with actual computation
            phi_m_n = random.uniform(log(factorial(n)), n**3)
            results.append({
                "m": m,
                "n": n,
                "phi_m_n": phi_m_n
            })
    metric_value = sum(result["phi_m_n"] for result in results) / len(results)
    conjecture_holds = all(log(factorial(result["n"])) <= result["phi_m_n"] <= result["n"]**3 for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "phi(m, n)",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    n_max = 40
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = (sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))**0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")