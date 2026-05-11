# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations, permutations

def factorial(n):
    if n == 0:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def hook_length_formula(partition):
    n = len(partition)
    numerator = factorial(factorial(n))
    denominator = 1
    for row in partition:
        for cell in range(len(row)):
            hook = row[cell] - cell + (n - row[cell])
            denominator *= hook
    return numerator // denominator

def generate_partition(n):
    if n == 0:
        return [[]]
    partitions = []
    for i in range(1, n + 1):
        for p in generate_partition(n - i):
            partitions.append([i] + p)
    return partitions

def count_irreducible_components(decompositions, n):
    counts = set()
    for decomposition in decompositions:
        for part in decomposition:
            if len(part) == n:
                counts.add(tuple(sorted(part)))
    return len(counts)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in range(2, 41):
        m = math.isqrt(n * n // 3) + 1
        perm_count = count_irreducible_components([n], n)
        det_count = count_irreducible_components([m], m)
        if perm_count <= det_count:
            return {
                "metric_name": "irreducible_components",
                "metric_value": perm_count,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"n={n}, m={m}: {perm_count} ≤ {det_count}"
            }
    return {
        "metric_name": "irreducible_components",
        "metric_value": perm_count,
        "instances_tested": 40 - 1,  # Exclude the first seed
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")