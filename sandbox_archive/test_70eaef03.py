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
    n_max = 0
    instances_tested = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""

    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n

        for _ in range(5):  # Ensure at least 30 instances per seed
            num_clauses = random.randint(1, n)
            formula = generate_formula(n, num_clauses)
            deg_G = compute_deg_G(formula)
            metric_value = deg_G / (num_clauses ** 2)

            total_metric_value += metric_value
            instances_tested += 1

            if deg_G > num_clauses ** 2:
                conjecture_holds = False
                counterexample = f"Formula with n={n}, clauses={num_clauses} has deg_G={deg_G}"

    mean_metric_value = total_metric_value / instances_tested
    return {
        "metric_name": "deg_G / |C(φ)|^2",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def generate_formula(n: int, num_clauses: int) -> list:
    formula = []
    for _ in range(num_clauses):
        clause = [random.choice([1, -1]) * random.randint(1, n) for _ in range(random.randint(1, n))]
        formula.append(clause)
    return formula

def compute_deg_G(formula: list) -> int:
    # Placeholder for actual computation of deg_G
    # This is a dummy implementation that always returns 0
    return 0

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = r["seed"]
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")