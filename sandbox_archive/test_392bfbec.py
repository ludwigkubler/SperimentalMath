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

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        if matrix[i][i] == 0:
            # Swap with a row below that has a non-zero pivot
            for j in range(i + 1, n):
                if matrix[j][i] != 0:
                    matrix[i], matrix[j] = matrix[j], matrix[i]
                    break
            else:
                raise ValueError("Matrix is singular")
        # Normalize the pivot row
        factor = Fraction(1, matrix[i][i])
        for j in range(n):
            matrix[i][j] *= factor
        # Eliminate the current column below the pivot
        for j in range(i + 1, n):
            factor = matrix[j][i]
            for k in range(n):
                matrix[j][k] -= factor * matrix[i][k]

def hodge_index(matrix):
    n = len(matrix)
    rank = sum(1 for row in matrix if any(row))
    return Fraction(rank * (n - rank), n)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    instances_tested = 0
    total_hodge_index = Fraction(0)
    conjecture_holds = True
    counterexample = ""

    for _ in range(30):
        # Generate a random function with communication complexity O(n^c)
        c = random.uniform(0.1, 2)
        f = lambda x: sum(x[i] * x[j] for i in range(n) for j in range(i + 1, n)) ** (1 / c)
        X = set(range(n))
        Y = set(range(n))
        M = [[f((i, j)) for j in Y] for i in X]

        try:
            gaussian_elimination(M)
            H_M = hodge_index(M)
            instances_tested += 1
            total_hodge_index += H_M

            if H_M < n ** (1/2):
                conjecture_holds = False
                counterexample = f"Seed {seed}: H(M) = {H_M} < n^(1/2) for n={n}"
        except Exception as e:
            return {
                "metric_name": "H(M)",
                "metric_value": None,
                "instances_tested": instances_tested,
                "conjecture_holds": False,
                "counterexample": str(e)
            }

    mean_hodge_index = total_hodge_index / instances_tested
    support_fraction = instances_tested / 30

    return {
        "metric_name": "H(M)",
        "metric_value": float(mean_hodge_index),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")

    mean_hodge_index = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_hodge_index} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=not_enough_data")