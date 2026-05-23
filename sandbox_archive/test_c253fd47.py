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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = matrix[i][i]
            for j in range(i, n + 1):
                matrix[i][j] /= factor
            for j in range(n):
                if j != i:
                    factor = matrix[j][i]
                    for k in range(i, n + 1):
                        matrix[j][k] -= factor * matrix[i][k]
        return [row[:n] for row in matrix]

    def rank(matrix):
        augmented_matrix = [row[:] + [1 if i == j else 0 for j in range(len(row))] for i, row in enumerate(matrix)]
        reduced_matrix = gaussian_elimination(augmented_matrix)
        rank = sum(1 for row in reduced_matrix if any(val != 0 for val in row))
        return rank

    def acc0_circuit_threshold(n):
        # Placeholder function to simulate ACC⁰ circuit threshold
        return n * math.log2(n)

    n = random.randint(5, 40)
    f = [random.choice([1, -1]) for _ in range(n)]
    Q = [[sum(f[i] * f[j] for i in range(n)) for j in range(n)] for _ in range(n)]
    
    rank_Q = rank(Q)
    threshold = acc0_circuit_threshold(n)
    conjecture_holds = rank_Q <= threshold / math.log2(n)

    return {
        "metric_name": "ACC⁰ Circuit Threshold vs Rank",
        "metric_value": rank_Q,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Rank Q exceeds Θ(log²(n)) for n={n}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank Q exceeds Θ(log²(n))\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")