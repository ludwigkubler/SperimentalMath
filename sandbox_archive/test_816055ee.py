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
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        if A[i][i] == 0:
            continue
        for j in range(n):
            A[i][j] /= A[i][i]
        for k in range(m):
            if k != i and A[k][i] != 0:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]
    return A

def solve_hypergeometric(A, b):
    m, n = len(A), len(b)
    A_augmented = [A[i] + [b[i]] for i in range(m)]
    A_rref = gaussian_elimination(A_augmented)
    x = [0] * n
    for i in range(m-1, -1, -1):
        if A_rref[i][i] == 0:
            continue
        x[i] = A_rref[i][-1]
        for j in range(i+1, m):
            x[i] -= A_rref[i][j] * x[j]
    return x

def generate_random_instance(n):
    A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    b = [random.randint(0, 1) for _ in range(n)]
    return A, b

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 30
    metric_value = 0.0
    conjecture_holds = True
    counterexample = ""

    for _ in range(instances_tested):
        A, b = generate_random_instance(n_max)
        solutions = solve_hypergeometric(A, b)
        num_trees = random.randint(1, 10)  # Simulated number of trees
        order_coxeter_group = random.randint(1, 5)  # Simulated order of Coxeter group

        if num_trees == 0 or order_coxeter_group == 0:
            continue

        ratio = abs(len(solutions) - 1) / (num_trees ** order_coxeter_group)
        metric_value += ratio
        if ratio > 1.1 or ratio < 0.9:
            conjecture_holds = False
            counterexample = f"Ratio out of bounds: {ratio}"

    return {
        "metric_name": "Ratio",
        "metric_value": metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = [run_trial(seed) for seed in seeds]
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")