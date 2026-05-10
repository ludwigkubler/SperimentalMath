# auto-injected by SEC sandbox
import math
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from collections import defaultdict

def generate_3sat_instance(n: int, m: int) -> list:
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, 3)
        if random.choice([True, False]):
            clause[0] *= -1
        if random.choice([True, False]):
            clause[1] *= -1
        if random.choice([True, False]):
            clause[2] *= -1
        clauses.append(clause)
    return clauses

def dpll(sat_formula: list) -> int:
    def solve(model):
        for literal in model:
            if literal == 0:
                return None
        satisfied = True
        for clause in sat_formula:
            clause_satisfied = False
            for literal in clause:
                if literal > 0 and literal in model or literal < 0 and -literal not in model:
                    clause_satisfied = True
                    break
            if not clause_satisfied:
                return None
        return model

    def backtrack(model):
        free_vars = [var for var in range(1, n + 1) if var not in model]
        if not free_vars:
            return solve(model)
        var = free_vars[0]
        model[var] = True
        result = backtrack(model)
        if result is not None:
            return result
        del model[var]
        model[-var] = True
        result = backtrack(model)
        if result is not None:
            return result
        return None

    n = len(sat_formula[0])
    return backtrack({})

def hilbert_function(n: int, d: int) -> int:
    # Placeholder for actual Hilbert function computation
    return 1  # Simplified for testing purposes

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    m = 3 * n // 2
    sat_formula = generate_3sat_instance(n, m)
    solutions_count = dpll(sat_formula)
    if solutions_count is None:
        return {
            "metric_name": "H_I(d)",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "DPLL failed to find a solution"
        }
    h_i_n2 = hilbert_function(n, n // 2)
    if solutions_count == 0:
        return {
            "metric_name": "H_I(d)",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "No solutions found"
        }
    metric_value = h_i_n2 / solutions_count
    conjecture_holds = abs(metric_value - 1) < 0.1  # Simplified threshold for testing purposes
    return {
        "metric_name": "H_I(d)",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results)) ** 0.5
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")