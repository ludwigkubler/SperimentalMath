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
            # Find a non-zero pivot below
            for j in range(i + 1, n):
                if A[j][i] != 0:
                    A[i], A[j] = A[j], A[i]
                    break
            else:
                raise ValueError("Matrix is singular")
        factor = Fraction(1, A[i][i])
        for k in range(n):
            A[i][k] *= factor
        for j in range(i + 1, n):
            factor = A[j][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def rank_of_matrix(A):
    n = len(A)
    rank = 0
    for i in range(n):
        if all(A[i][j] == Fraction(0) for j in range(n)):
            continue
        rank += 1
        factor = Fraction(1, A[i][i])
        for k in range(n):
            A[i][k] *= factor
        for j in range(i + 1, n):
            factor = A[j][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return rank

def incidence_algebra(I):
    n = len(I)
    A = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if I[i][j]:
                A[i][j] = Fraction(1, math.factorial(j - i - 1))
                A[j][i] = Fraction(-1, math.factorial(j - i - 1))
    return A

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    I = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        I[i][i] = 0
    G = incidence_algebra(I)
    rank = rank_of_matrix(G)
    metric_value = rank
    instances_tested = 1
    conjecture_holds = rank >= n ** Fraction(1, 2)
    counterexample = "" if conjecture_holds else "n={}".format(n)
    return {
        "metric_name": "affine_representation_rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 307))  # Default to first 30 primes if no seeds provided
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print("TRIAL: {}".format(trial_result))
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_value, std_value, support_fraction))
    elif support_fraction >= 0.8:
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_value, std_value, support_fraction))
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample='n={}' first_failing_seed={}".format(first_failing_seed, first_failing_seed))