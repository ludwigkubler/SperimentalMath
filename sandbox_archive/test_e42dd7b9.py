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
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        factor = Fraction(1, A[i][i])
        for j in range(n):
            A[i][j] *= factor
        for j in range(n):
            if i != j:
                factor = -A[j][i]
                for k in range(n):
                    A[j][k] += factor * A[i][k]

def matrix_multiplication(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def distillable_entropy(state):
    n = len(state)
    v = [Fraction(1, n)] * n
    Av = matrix_multiplication(state, v)
    epsilon = 0
    for i in range(n):
        epsilon += abs(Av[i] - Fraction(1, n))
    return epsilon

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    state = [[random.random() for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            state[i][j] = state[j][i]
            state[j][i] = state[i][j]
    epsilon = distillable_entropy(state)
    if epsilon <= 0:
        return {
            "metric_name": "tau",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "epsilon_non_positive"
        }
    tau = len([i for i in range(n) if state[i][i] != 0])
    return {
        "metric_name": "tau",
        "metric_value": tau,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_tau = sum(r["metric_value"] for r in results) / len(results)
    std_tau = math.sqrt(sum((r["metric_value"] - mean_tau)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_tau} std={std_tau} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        counterexample = next(r for r in results if not r["conjecture_holds"])["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[results.index(next(r for r in results if not r['conjecture_holds']))]}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")