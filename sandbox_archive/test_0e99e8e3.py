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

def gaussian_elimination(A):
    n = len(A)
    A_copy = [row[:] for row in A]
    for i in range(n):
        if A_copy[i][i] == 0:
            return None  # Singular matrix
        for j in range(i + 1, n):
            factor = -A_copy[j][i] / A_copy[i][i]
            for k in range(n):
                A_copy[j][k] += factor * A_copy[i][k]
    rank = sum(1 for row in A_copy if any(row))
    return rank

def multivariate_continued_fraction(n, seed):
    random.seed(seed)
    A = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
    return gaussian_elimination(A)

def run_trial(seed: int) -> dict:
    n_values = [5, 10, 15, 20, 30, 40]
    total_amplification = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):  # Test 5 instances per size
            r = multivariate_continued_fraction(n, seed)
            if r is None:
                return {
                    "metric_name": "amplitude_amplification",
                    "metric_value": None,
                    "instances_tested": instances_tested,
                    "conjecture_holds": False,
                    "counterexample": "mapping_undefined"
                }
            A = random.random()  # Simulate amplitude amplification factor
            total_amplification += A
            instances_tested += 1
            if A > 1 / (r + 2):
                conjecture_holds = False
                counterexample = f"A={A} > 1/({r}+2)"

    average_rank = sum([multivariate_continued_fraction(n, seed) for n in n_values]) / len(n_values)
    average_amplification = total_amplification / instances_tested

    return {
        "metric_name": "amplitude_amplification",
        "metric_value": average_amplification,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds and average_amplification <= 1 / (average_rank + 2),
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(res["metric_value"] for res in results if res["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results if res["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{res['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")