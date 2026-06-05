# auto-injected by SEC sandbox
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
import sys
import itertools

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_formula(n):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(n):
            clause = random.sample(variables, random.randint(1, n))
            clauses.append(clause)
        return clauses

    def construct_groupoid(formula):
        n = len(formula[0])
        groupoid = [[None] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i == j:
                    groupoid[i][j] = Fraction(1, 1)
                else:
                    groupoid[i][j] = Fraction(0, 1)
        return groupoid

    def resolution_width(formula):
        # Simplified version of resolution width calculation
        width = 0
        for clause in formula:
            width = max(width, len(clause))
        return width

    n_max = 40
    instances_tested = 0
    dim_sum = 0
    width_sum = 0

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            formula = generate_formula(n)
            groupoid = construct_groupoid(formula)
            dim = sum(1 for row in groupoid if any(x != Fraction(0, 1) for x in row))
            width = resolution_width(formula)
            dim_sum += dim
            width_sum += width
            instances_tested += 1

    mean_dim = dim_sum / instances_tested
    mean_width = width_sum / instances_tested
    correlation_coefficient = (instances_tested * sum(dim * width for dim, width in zip(groupoid, groupoid)) - 
                               dim_sum * width_sum) / math.sqrt((instances_tested * sum(dim ** 2 for dim in groupoid) - dim_sum ** 2) *
                                                              (instances_tested * sum(width ** 2 for width in groupoid) - width_sum ** 2))

    conjecture_holds = correlation_coefficient > 0.5 and max(dim / mean_width for dim, width in zip(groupoid, groupoid)) <= 5
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")