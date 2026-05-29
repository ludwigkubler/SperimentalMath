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
    
    def generate_boolean_function(n):
        # Generate a boolean function with arithmetic progression symmetry
        coefficients = [random.choice([0, 1]) for _ in range(n)]
        differences = set()
        for i in range(1, n):
            diff = coefficients[i] - coefficients[i-1]
            if diff != 0:
                differences.add(diff)
        return coefficients, len(differences)

    def tree_like_resolution_width(coefficients):
        # Simplified version of tree-like resolution width calculation
        n = len(coefficients)
        width = 0
        for i in range(n):
            if coefficients[i] == 1:
                width += 1
        return width

    instances_tested = 30
    t_star_values = []
    S_values = []

    for _ in range(instances_tested):
        n = random.choice([5, 10, 15, 20, 30, 40])
        coefficients, S = generate_boolean_function(n)
        t_star = tree_like_resolution_width(coefficients)
        t_star_values.append(t_star)
        S_values.append(S)

    mean_t_star = sum(t_star_values) / instances_tested
    std_t_star = math.sqrt(sum((x - mean_t_star) ** 2 for x in t_star_values) / instances_tested)
    upper_bound = math.log(max(S_values) ** 2, 2)

    conjecture_holds = mean_t_star <= upper_bound and std_t_star / mean_t_star < 0.1
    counterexample = f"t_star={mean_t_star}, upper_bound={upper_bound}" if not conjecture_holds else ""

    return {
        "metric_name": "t_star",
        "metric_value": mean_t_star,
        "instances_tested": instances_tested,
        "n_max": max(S_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_t_star = sum(r["metric_value"] for r in results) / len(results)
    std_t_star = math.sqrt(sum((r["metric_value"] - mean_t_star) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_t_star} std={std_t_star} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")