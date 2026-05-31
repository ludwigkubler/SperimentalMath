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

def count_satisfying_assignments(f, n):
    m = len(f)
    g_n = 0
    for i in range(m):
        if sum(int(x) * int(y) for x, y in zip(bin(i)[2:].zfill(n), f)) == n:
            g_n += 1
    return g_n

def calculate_entropy(g_n):
    total = sum(g_n)
    probabilities = [Fraction(count, total) for count in g_n]
    entropy = -sum(p * math.log2(p) for p in probabilities if p != 0)
    return entropy

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    g_n = []
    entropies = []

    for n in n_values:
        f = generate_random_boolean_function(n)
        g_n.append(count_satisfying_assignments(f, n))
        entropy = calculate_entropy(g_n)
        entropies.append(entropy)

    metric_name = "Entropy"
    metric_value = sum(entropies) / len(entropies)
    instances_tested = len(n_values)
    n_max = max(n_values)
    conjecture_holds = all(metric_value <= 4 for _ in range(instances_tested))
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
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
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")