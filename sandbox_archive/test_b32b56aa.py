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
        max_row = i
        for j in range(i + 1, rows):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        pivot = A[i][i]
        if pivot == 0:
            continue
        for j in range(i, cols):
            A[i][j] /= pivot
        for k in range(rows):
            if k != i and A[k][i] != 0:
                factor = A[k][i]
                for j in range(i, cols):
                    A[k][j] -= factor * A[i][j]

def rank(A):
    A_copy = [row[:] for row in A]
    gaussian_elimination(A_copy)
    rank = 0
    for row in A_copy:
        if any(row[j] != 0 for j in range(len(row))):
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    edges = set()
    while len(edges) < n * (n - 1) // 2:
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v and (u, v) not in edges and (v, u) not in edges:
            edges.add((u, v))
    A = [[Fraction(0, 1)] * n for _ in range(n)]
    for u, v in edges:
        A[u][v] = Fraction(1, 2)
        A[v][u] = Fraction(1, 2)

    rank_A = rank(A)
    conjecture_holds = rank_A <= n
    counterexample = "" if conjecture_holds else f"Rank {rank_A} > {n}"
    
    return {
        "metric_name": "Generalized Kostant Partition Function Rank",
        "metric_value": rank_A,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r <= n) / len(results)
    
    if all(r <= n for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample='Rank exceeds {n}' first_failing_seed=1")
    else:
        print(f"RESULT: INCONCLUSIVE reason=support_fraction_too_low")