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

def sign_matrix(n):
    return [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]

def hadamard_matrix(n):
    if n == 1:
        return [[1]]
    H = hadamard_matrix(n // 2)
    top_left = H
    top_right = H
    bottom_left = H
    bottom_right = [-x for x in H]
    return [
        [top_left[i][j] + top_right[i][j] for j in range(n // 2)] +
        [top_left[i][j] - top_right[i][j] for j in range(n // 2)]
        for i in range(n // 2)
    ] + [
        [bottom_left[i][j] + bottom_right[i][j] for j in range(n // 2)] +
        [bottom_left[i][j] - bottom_right[i][j] for j in range(n // 2)]
        for i in range(n // 2)
    ]

def dyadic_boxes(n):
    boxes = []
    for i in range(n + 1):
        for j in range(n + 1):
            boxes.append((i, j))
    return boxes

def star_discrepancy(M):
    n = len(M)
    boxes = dyadic_boxes(n)
    max_disc = 0
    for i, j in boxes:
        box_sum = sum(M[x][y] for x in range(i, min(n, i + 2)) for y in range(j, min(n, j + 2)))
        disc = abs(box_sum) / math.sqrt((i + 1) * (j + 1))
        if disc > max_disc:
            max_disc = disc
    return max_disc

def rank(matrix):
    n = len(matrix)
    A = [row[:] for row in matrix]
    pivot_row = 0
    for j in range(n):
        i = pivot_row
        while i < n and A[i][j] == 0:
            i += 1
        if i == n:
            continue
        A[pivot_row], A[i] = A[i], A[pivot_row]
        for k in range(j + 1, n):
            A[pivot_row][k] /= A[pivot_row][j]
        for i in range(n):
            if i != pivot_row:
                factor = A[i][j]
                for k in range(j, n):
                    A[i][k] -= factor * A[pivot_row][k]
        pivot_row += 1
    return pivot_row

def perturb_matrix(M, w):
    n = len(M)
    indices = list(range(n * n))
    random.shuffle(indices)
    for k in range(w):
        i, j = divmod(indices[k], n)
        M[i][j] *= -1
    return M

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [4, 8, 16]:
        H_n = hadamard_matrix(n)
        D_H_n = star_discrepancy(H_n)
        R_H_n_n2 = rank(perturb_matrix(H_n, int(0.5 * n**2)))
        results.append({
            "n": n,
            "D_H_n": D_H_n,
            "R_H_n_n2": R_H_n_n2,
            "ratio": R_H_n_n2 * math.log(n) / D_H_n**2
        })
    return {
        "metric_name": "ratio",
        "metric_value": sum(result["ratio"] for result in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": all(result["ratio"] >= 0.05 for result in results),
        "counterexample": "" if all(result["ratio"] >= 0.05 for result in results) else "Hadamard matrix"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or [11, 23, 37, 53, 71]
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")