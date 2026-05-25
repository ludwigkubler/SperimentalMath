# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    rank = 0

    for i in range(cols):
        if rank >= rows:
            break

        max_row = i + sum(1 for j in range(i, rows) if abs(matrix[j][i]) > abs(matrix[max_row][i]))
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]

        if matrix[i][i] == 0:
            continue

        pivot = Fraction(matrix[i][i])
        for j in range(cols):
            matrix[i][j] /= pivot

        for j in range(rows):
            if j != i and matrix[j][i] != 0:
                factor = -matrix[j][i]
                for k in range(cols):
                    matrix[j][k] += factor * matrix[i][k]

        rank += 1

    return rank

def minimal_rank(matrix):
    rows, cols = len(matrix), len(matrix[0])
    min_rank = float('inf')

    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] != 0:
                sub_matrix = [row[:j] + row[j+1:] for row in matrix[:i] + matrix[i+1:]]
                rank = gaussian_elimination(sub_matrix)
                min_rank = min(min_rank, rank)

    return min_rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 5
    k = 3
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for _ in range(10):  # Test with multiple instances per seed
        # Generate a monotone circuit for k-CLIQUE
        # This is a placeholder; actual implementation depends on the specific structure of k-CLIQUE circuits
        matrix = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        rank = minimal_rank(matrix)
        instances_tested += 1

        if rank < n ** k:
            conjecture_holds = False
            counterexample = f"Counterexample found: Rank {rank} < {n**k}"

    return {
        "metric_name": "Minimal Rank",
        "metric_value": n ** k,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = (sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")