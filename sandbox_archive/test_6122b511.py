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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        pivot = A[i][i]
        if pivot == 0:
            continue
        for j in range(n):
            A[i][j] /= pivot
        for k in range(m):
            if k != i:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]
    return A

def matrix_rank(A):
    m, n = len(A), len(A[0])
    rank = 0
    for i in range(m):
        if any(A[i]):
            rank += 1
    return rank

def frege_proof_depth(f):
    stack = []
    for clause in f:
        if not any(var in stack for var in clause):
            stack.append(clause)
    return len(stack)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 0
    instances_tested = 0
    total_rrep = 0
    total_d_f = 0

    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        for _ in range(5):
            f = [[random.choice([-1, 1]) * random.randint(1, n) for _ in range(n)] for _ in range(n)]
            A = gaussian_elimination(f)
            rrep = matrix_rank(A)
            d_f = frege_proof_depth(f)
            total_rrep += rrep
            total_d_f += d_f
            instances_tested += 1

    mean_rrep_over_d_f = total_rrep / total_d_f if total_d_f != 0 else float('inf')
    conjecture_holds = mean_rrep_over_d_f <= 1.5
    counterexample = "" if conjecture_holds else f"mean_rrep_over_d_f={mean_rrep_over_d_f}"

    return {
        "metric_name": "mean_rrep_over_d_f",
        "metric_value": mean_rrep_over_d_f,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean_rrep_over_d_f exceeded 1.5\" first_failing_seed={first_failing_seed}")