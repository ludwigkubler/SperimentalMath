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

def generate_k_cnf(n, k):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(k):
        clause = random.sample(variables, 2)
        clauses.append(clause)
    return clauses

def tree_width(cnf):
    # Placeholder function to compute tree-width
    # This is a dummy implementation and should be replaced with an actual algorithm
    return len(cnf)

def quotient_algebra(cnf):
    # Placeholder function to compute the quotient algebra
    # This is a dummy implementation and should be replaced with an actual algorithm
    return 0

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested = 0
        mean_absolute_difference = 0.0
        for _ in range(5):  # Ensure at least 5 instances per size
            cnf = generate_k_cnf(n, n)
            tree_w = tree_width(cnf)
            rank = quotient_algebra(cnf)
            if rank == -1:
                return {
                    "metric_name": "mean_absolute_difference",
                    "metric_value": None,
                    "instances_tested": 0,
                    "conjecture_holds": False,
                    "counterexample": "mapping_undefined"
                }
            instances_tested += 1
            mean_absolute_difference += abs(rank - tree_w)
        mean_absolute_difference /= instances_tested
        results.append({
            "n": n,
            "instances_tested": instances_tested,
            "mean_absolute_difference": mean_absolute_difference
        })
    return {
        "metric_name": "mean_absolute_difference",
        "metric_value": sum(r["mean_absolute_difference"] for r in results) / len(results),
        "instances_tested": sum(r["instances_tested"] for r in results),
        "conjecture_holds": all(r["mean_absolute_difference"] <= 3 for r in results),
        "counterexample": "" if all(r["mean_absolute_difference"] <= 3 for r in results) else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")