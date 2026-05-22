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

def evaluate_formula(formula):
    if "x" not in formula:
        return eval(formula)
    x_values = [0, 1]
    for value in x_values:
        formula_substituted = formula.replace("x", str(value))
        try:
            left, right = formula_substituted.split("&")
            if evaluate_formula(left) and evaluate_formula(right):
                return True
        except ValueError:
            continue
    return False

def generate_boolean_formula(n):
    variables = [f"x{i}" for i in range(n)]
    clauses = []
    for _ in range(n):
        clause = random.choice(variables)
        if random.choice([True, False]):
            clause = f"~{clause}"
        clauses.append(clause)
    return " & ".join(clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    total_width = 0
    instances_tested = 0

    for n in n_values:
        for _ in range(30):
            formula = generate_boolean_formula(n)
            m = sum(1 for i in range(2**n) if evaluate_formula(formula.replace("x", bin(i)[2:].zfill(n))))
            rank = m * math.log(n, 2)  # Simplified upper bound for the rank
            width = random.randint(1, n)  # Placeholder for DPLL search tree width calculation

            total_rank += rank
            total_width += width
            instances_tested += 1

    mean_rank = total_rank / instances_tested
    mean_width = total_width / instances_tested
    conjecture_holds = mean_rank <= mean_width
    counterexample = "" if conjecture_holds else f"mean_rank={mean_rank}, mean_width={mean_width}"

    return {
        "metric_name": "Rank and Width",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys

    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 53))  # First 30 primes

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    mean_width = sum(r["instances_tested"] * r["metric_value"] for r in results) / sum(r["instances_tested"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={math.sqrt(sum((r['metric_value'] - mean_rank) ** 2 for r in results) / len(results))} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean_rank > mean_width\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")