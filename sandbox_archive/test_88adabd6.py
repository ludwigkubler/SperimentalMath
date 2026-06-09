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

def generate_cnf(n, m):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, 2)
        clauses.append(clause)
    return clauses

def dpll(cnf):
    def solve(model, clauses):
        if not clauses:
            return model
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            var = unit_clause[0]
            new_model = {**model, var: True}
            return solve(new_model, [c for c in clauses if var not in c])
        pure_literal = next((v for v in variables if all(v not in c or not model.get(-v) for c in clauses)), None)
        if pure_literal:
            new_model = {**model, pure_literal: True}
            return solve(new_model, [c for c in clauses if pure_literal not in c])
        var = random.choice(variables)
        new_model_true = {**model, var: True}
        result_true = solve(new_model_true, clauses)
        if result_true:
            return result_true
        new_model_false = {**model, var: False}
        return solve(new_model_false, clauses)
    
    variables = list(range(1, len(cnf) + 1))
    return solve({}, cnf)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    R_values = []
    d_values = []

    for n in n_values:
        m = n * (n - 1) // 2
        cnf = generate_cnf(n, m)
        model = dpll(cnf)
        if model is None:
            return {
                "metric_name": "R",
                "metric_value": 0,
                "instances_tested": 0,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "dpll returned None"
            }
        R = len(model)
        R_values.append(R)

        # Calculate Frege proof depth (simplified example)
        d = n * m
        d_values.append(d)

    metric_value = sum(R_values) / len(R_values)
    instances_tested = len(R_values)
    n_max = max(n_values)
    conjecture_holds = abs(sum(r - d for r, d in zip(R_values, d_values))) < 0.1 * instances_tested
    counterexample = "" if conjecture_holds else "dpll returned None"

    return {
        "metric_name": "R",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"dpll returned None\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unsupported")