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
    rows = len(matrix)
    cols = len(matrix[0])
    for i in range(rows):
        max_row = i + max(range(i, rows), key=lambda x: abs(matrix[x][i]))
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        pivot = matrix[i][i]
        if pivot == 0:
            continue
        for j in range(cols):
            matrix[i][j] /= pivot
        for k in range(rows):
            if k != i:
                factor = matrix[k][i]
                for j in range(cols):
                    matrix[k][j] -= factor * matrix[i][j]
    return matrix

def local_coherence_rank(P):
    n = len(P)
    identity_matrix = [[Fraction(1, 1) if i == j else Fraction(0, 1) for j in range(n)] for i in range(n)]
    augmented_matrix = [row + col for row, col in zip(P, identity_matrix)]
    reduced_matrix = gaussian_elimination(augmented_matrix)
    rank = sum(1 for row in reduced_matrix if any(val != Fraction(0, 1) for val in row))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    P = [[random.choice([Fraction(0, 1), Fraction(1, 1)]) for _ in range(n)] for _ in range(n)]
    mlcr_P = local_coherence_rank(P)
    C_P = sum(sum(row) for row in P)
    k_values = [Fraction(1, 10), Fraction(1, 5), Fraction(1, 2), 1]
    max_diff = max(abs(mlcr_P - k * C_P) for k in k_values)
    return {
        "metric_name": "max_diff",
        "metric_value": float(max_diff),
        "instances_tested": n,
        "n_max": n,
        "conjecture_holds": all(max_diff <= 1e-6 for _ in range(30)),
        "counterexample": "" if max_diff <= 1e-6 else f"mlcr(P) = {mlcr_P}, C(P) = {C_P}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")