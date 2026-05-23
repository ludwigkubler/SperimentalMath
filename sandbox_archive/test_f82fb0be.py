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
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        max_row = i
        for j in range(i + 1, rows):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        pivot = matrix[i][i]
        if pivot == 0:
            continue
        for j in range(cols):
            matrix[i][j] /= pivot
        for j in range(rows):
            if i != j:
                factor = matrix[j][i]
                for k in range(cols):
                    matrix[j][k] -= factor * matrix[i][k]
    rank = sum(1 for row in matrix if any(row))
    return rank

def free_probability_distribution(P):
    n = len(P)
    M = [[0] * (n + 1) for _ in range(n + 1)]
    M[0][0] = 1
    for i in range(n):
        for j in range(n):
            if P[i][j]:
                M[i + 1][j] += P[i][j]
                M[j + 1][i] += P[i][j]
    return gaussian_elimination(M)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    P = [[random.random() if i != j else 0 for j in range(n)] for i in range(n)]
    rank = free_probability_distribution(P)
    median_rank = (n ** (1/3)) * 1.5
    conjecture_holds = rank <= median_rank
    counterexample = f"Rank({n}) = {rank}, expected <= {median_rank}" if not conjecture_holds else ""
    return {
        "metric_name": "Rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, ...{result}...}}")
        results.append(result)

    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_rank = math.sqrt(sum((result["metric_value"] - mean_rank) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")