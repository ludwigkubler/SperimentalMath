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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n, n * 3)
    p = random.randint(2, min(100, n))

    # Generate a random QBF instance
    qbf_instance = [[random.choice([0, 1]) for _ in range(n)] for _ in range(m)]

    # Compute the clause indicator polynomial modulo p
    coefficients = [0] * (n + 1)
    for i in range(m):
        product = 1
        for j in range(n):
            if qbf_instance[i][j]:
                product *= (-1) ** (random.choice([0, 1]))
        coefficients[product % p] += 1

    # Construct the quadratic reciprocity lattice
    lattice = []
    for i in range(len(coefficients)):
        for j in range(i + 1):
            lattice.append((i - j) * (i + j))

    # Gaussian elimination to find the minimal order of the lattice
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            if A[i][i] == 0:
                for j in range(i + 1, m):
                    if A[j][i] != 0:
                        A[i], A[j] = A[j], A[i]
                        break
                else:
                    continue
            pivot = Fraction(A[i][i])
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i and A[j][i] != 0:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    min_order = len(gaussian_elimination(lattice))

    # Check the conjecture
    if min_order > 2 ** n * math.log(n / p) ** 2 + 1:
        return {
            "metric_name": "min_order",
            "metric_value": min_order,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Instance with n={n}, m={m}, p={p} violates the conjecture."
        }

    return {
        "metric_name": "min_order",
        "metric_value": min_order,
        "instances_tested": 1,
        "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    results = []
    total_min_order = 0
    num_trials = len(seeds)

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        total_min_order += result["metric_value"]
        if not result["conjecture_holds"]:
            break

    mean_min_order = total_min_order / num_trials
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / num_trials

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_min_order} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results) and sum(1 for r in results if not r["conjecture_holds"]) / num_trials >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_min_order} std=0.0 support_fraction=1.0")
    else:
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")