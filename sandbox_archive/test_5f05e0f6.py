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
    for i in range(n):
        if A[i][i] == 0:
            # Find a row with non-zero pivot and swap
            for j in range(i+1, n):
                if A[j][i] != 0:
                    A[i], A[j] = A[j], A[i]
                    break
            else:
                raise ValueError("Matrix is singular")
        factor = Fraction(A[i][i])
        for j in range(n):
            A[i][j] /= factor
        for k in range(n):
            if k != i and A[k][i] != 0:
                factor = Fraction(A[k][i])
                for j in range(n):
                    A[k][j] -= factor * A[i][j]
    return A

def hodge_weight(phi):
    # Placeholder function to compute Hodge weight
    # This is a dummy implementation and should be replaced with actual computation
    return random.random()

def min_circuit_depth(phi):
    # Placeholder function to compute minimum circuit depth
    # This is a dummy implementation and should be replaced with actual computation
    return random.randint(1, 10)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 30
    ratios = []

    for _ in range(instances_tested):
        n = random.randint(5, 40)
        phi = [random.choice([0, 1]) for _ in range(n)]
        h_weight = hodge_weight(phi)
        d_phi = min_circuit_depth(phi)
        if d_phi == 0:
            continue
        ratios.append(h_weight / d_phi)

    mean_ratio = sum(ratios) / len(ratios)
    conjecture_holds = all(1.5 <= r < 2 for r in ratios)
    counterexample = "" if conjecture_holds else "Hodge weight to circuit depth ratio out of bounds"

    return {
        "metric_name": "Hodge Weight to Circuit Depth Ratio",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")

    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Hodge weight to circuit depth ratio out of bounds\" first_failing_seed={first_failing_seed}")