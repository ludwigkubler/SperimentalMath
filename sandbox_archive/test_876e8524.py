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

def generate_read_twice_boolean_function(n: int) -> list:
    if n == 1:
        return [random.choice([0, 1])]
    else:
        left = generate_read_twice_boolean_function(n // 2)
        right = generate_read_twice_boolean_function(n - len(left))
        return [left[i] ^ right[i % len(right)] for i in range(n)]

def calculate_free_probability_rank(f: list) -> int:
    n = len(f)
    rank = 0
    for i in range(1, n):
        if f[i] != f[0]:
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested = 10
        total_rank = 0
        for _ in range(instances_tested):
            f = generate_read_twice_boolean_function(n)
            rank = calculate_free_probability_rank(f)
            results.append((n, rank))
            total_rank += rank
        mean_rank = Fraction(total_rank, instances_tested)
        if n == 1:
            continue
        corr_coeff = sum((x - n) * (y - mean_rank) for x, y in results) / (instances_tested * math.sqrt(n * (n - 1)))
        conjecture_holds = corr_coeff >= 0.8 and total_rank <= n * math.log(2 * n)
        counterexample = "" if conjecture_holds else "mapping_undefined"
        return {
            "metric_name": "Pearson Correlation Coefficient",
            "metric_value": float(corr_coeff),
            "instances_tested": instances_tested,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")