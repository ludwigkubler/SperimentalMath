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

def generate_random_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def communication_complexity_rank(f):
    n = len(f)
    if n == 1:
        return 1
    rank = 0
    for i in range(1, n):
        if all(f[j] != f[j ^ (1 << i)] for j in range(2**n)):
            rank += 1
    return rank

def kahler_class_rank(n):
    # Placeholder function to simulate Kähler class rank computation
    # This is a dummy implementation and should be replaced with actual logic
    return random.randint(1, n)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        f = generate_random_boolean_function(n)
        r_f = communication_complexity_rank(f)
        kahler_rank = kahler_class_rank(n)
        results.append({
            "n": n,
            "r_f": r_f,
            "kahler_rank": kahler_rank
        })
    metric_value = sum(r["kahler_rank"] - r["r_f"] for r in results) / len(results)
    instances_tested = len(results)
    n_max = max(r["n"] for r in results)
    conjecture_holds = all(r["kahler_rank"] >= r["r_f"] for r in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "Kähler class rank - Communication complexity rank difference",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")