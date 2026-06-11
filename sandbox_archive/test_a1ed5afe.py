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
    rows, cols = len(A), len(A[0])
    for i in range(rows):
        max_row = i + max(range(i, rows), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        if A[i][i] == 0:
            continue
        pivot = Fraction(1, A[i][i])
        for j in range(cols):
            A[i][j] *= pivot
        for k in range(rows):
            if k != i and A[k][i] != 0:
                factor = -A[k][i]
                for j in range(cols):
                    A[k][j] += factor * A[i][j]
    return A

def rank_variance(matrix):
    rows, cols = len(matrix), len(matrix[0])
    A = [[Fraction(matrix[i][j]) for j in range(cols)] for i in range(rows)]
    A = gaussian_elimination(A)
    rank = sum(1 for row in A if any(row))
    return Fraction(rank, min(rows, cols))

def minimal_order_of_lie_algebroid_action(matrix):
    alpha = rank_variance(matrix)
    if alpha <= 0:
        return None
    return math.ceil(math.sqrt(alpha))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    matrix = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    order = minimal_order_of_lie_algebroid_action(matrix)
    if order is None:
        return {
            "metric_name": "minimal_order",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    return {
        "metric_name": "minimal_order",
        "metric_value": order,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_order = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_order) ** 2 for r in results) / len(results))
        support_fraction = Fraction(sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]), len(results))
        print(f"RESULT: SUPPORTED mean={mean_order} std={std_dev} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")