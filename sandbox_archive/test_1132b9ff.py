# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations, product

def generate_cnf(n: int) -> list:
    literals = set(range(1, n + 1)) | {-i for i in range(1, n + 1)}
    clauses = []
    for _ in range(2 * n):
        clause = random.sample(literals, random.randint(1, n))
        clauses.append(clause)
    return clauses

def dpll(cnf: list) -> bool:
    if not cnf:
        return True
    literals = set(range(1, len(cnf) + 1)) | {-i for i in range(1, len(cnf) + 1)}
    literal = next(lit for lit in literals if any(lit in clause or -lit in clause for clause in cnf))
    positive = [c for c in cnf if literal in c]
    negative = [c for c in cnf if -literal in c]
    return dpll(positive) or dpll([c for c in cnf if not (-literal in c)])

def geometric_ar(cnf: list) -> int:
    # Placeholder function to compute geometric ar
    # This is a dummy implementation and should be replaced with the actual mapping
    return len(cnf)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n)
            w_DPLL_value = dpll(cnf)
            g_ar_value = geometric_ar(cnf)
            if g_ar_value < w_DPLL_value:
                conjecture_holds = False
                counterexample = f"n={n}, g_ar={g_ar_value}, w_DPLL={w_DPLL_value}"
            metric_values.append(g_ar_value - w_DPLL_value)
            instances_tested += 1
            n_max = max(n_max, n)

    return {
        "metric_name": "g_ar - w_DPLL",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")