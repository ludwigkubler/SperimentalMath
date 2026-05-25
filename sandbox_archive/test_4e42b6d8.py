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
    n = 10  # Start with a small size and increase if needed
    instances_tested = 0
    support_count = 0
    counterexample = ""

    for _ in range(30):
        formula = generate_random_cnf(n)
        hodge_norm = compute_tropical_hodge_norm(formula)
        resolution_length = compute_resolution_length(formula)

        if resolution_length == -1:
            continue

        instances_tested += 1
        ratio = hodge_norm / math.log(n)
        k = int(math.log(n))
        lower_bound = 2**k / math.log(n)

        if ratio < lower_bound:
            counterexample = f"CNF with n={n} requires fewer than {lower_bound} resolution steps."
            return {
                "metric_name": "Resolution Proof Length Ratio",
                "metric_value": ratio,
                "instances_tested": instances_tested,
                "conjecture_holds": False,
                "counterexample": counterexample
            }

        if ratio >= lower_bound:
            support_count += 1

    return {
        "metric_name": "Resolution Proof Length Ratio",
        "metric_value": support_count / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": support_count / instances_tested >= 0.8,
        "counterexample": counterexample
    }

def generate_random_cnf(n: int) -> list:
    clauses = []
    for _ in range(2**n):
        clause = [random.randint(-1, n-1) for _ in range(random.randint(1, n))]
        clauses.append(clause)
    return clauses

def compute_tropical_hodge_norm(cnf: list) -> float:
    # Placeholder implementation
    return random.random()

def compute_resolution_length(cnf: list) -> int:
    # Placeholder implementation
    return -1  # Indicates failure to compute length

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, ...run_trial output...}}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")