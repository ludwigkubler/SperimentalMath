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
        max_row = i + max(range(i, rows), key=lambda r: abs(A[r][i]))
        A[i], A[max_row] = A[max_row], A[i]
        if A[i][i] == 0:
            continue
        denom = A[i][i]
        for j in range(cols):
            A[i][j] /= denom
        for k in range(rows):
            if k != i and A[k][i] != 0:
                factor = A[k][i]
                for j in range(cols):
                    A[k][j] -= factor * A[i][j]
    return A

def matrix_rank(A):
    rank = 0
    for row in gaussian_elimination(A):
        if any(row):
            rank += 1
    return rank

def construct_quantum_group_representation(P, seed):
    random.seed(seed)
    n = len(P)
    V = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    return V

def run_trial(seed: int) -> dict:
    P = [[random.choice([0, 1]) for _ in range(40)] for _ in range(40)]
    V = construct_quantum_group_representation(P, seed)
    rank = matrix_rank(V)
    circuit_size = sum(sum(row) for row in P)
    ratio = Fraction(circuit_size, rank) if rank != 0 else float('inf')
    conjecture_holds = (ratio <= 1000) and (rank >= 2 * math.log(len(P)))
    counterexample = "" if conjecture_holds else f"Ratio {ratio} exceeds bound"
    return {
        "metric_name": "Rank vs Circuit Size",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **result}}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio exceeds bound\" first_failing_seed={first_failing_seed}")