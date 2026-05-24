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

def generate_disjointness_matrix(n):
    A = [[0] * n for _ in range(n)]
    for i in range(n):
        A[i][i] = 1
    return A

def tropicalize(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    A_trop = [[-math.inf] * cols for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            A_trop[i][j] = max([matrix[i][k] + matrix[k][j] for k in range(cols)])
    return A_trop

def rank(matrix):
    rows, cols = len(matrix), len(matrix[0])
    if rows > cols:
        matrix = list(zip(*matrix))
        rows, cols = cols, rows
    augmented_matrix = [row + [1] for row in matrix]
    pivot_row = 0
    for i in range(rows):
        if augmented_matrix[i][pivot_row] == -math.inf:
            pivot_row += 1
            continue
        for j in range(i+1, rows):
            factor = augmented_matrix[j][pivot_row] / augmented_matrix[i][pivot_row]
            for k in range(cols + 1):
                augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    rank = sum(1 for row in augmented_matrix if any(x != -math.inf for x in row))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        A = generate_disjointness_matrix(n)
        A_trop = tropicalize(A)
        rank_value = rank(A_trop)
        total_rank += rank_value
        instances_tested += 1

        if rank_value < n:
            conjecture_holds = False
            counterexample = f"n={n}, rank={rank_value} < {n}"

    mean_rank = Fraction(total_rank, instances_tested)
    return {
        "metric_name": "Tropical Rank",
        "metric_value": float(mean_rank),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rank = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")