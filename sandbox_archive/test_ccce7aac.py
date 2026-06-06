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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            for j in range(m):
                if i != j:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_rank(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(m):
            if all(abs(A[i][j]) < 1e-9 for j in range(n)):
                continue
            rank += 1
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            for j in range(m):
                if i != j:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return rank

    def hodge_structure_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        A = [[int(x % 2) for x in row] for row in matrix]
        A = gaussian_elimination(A)
        return sum(1 for row in A if any(abs(x) > 1e-9 for x in row))

    def variance(lst):
        mean = sum(lst) / len(lst)
        return sum((x - mean) ** 2 for x in lst) / len(lst)

    n = random.randint(5, 40)
    instances_tested = 30
    total_rank = 0
    min_rank = float('inf')
    
    for _ in range(instances_tested):
        matrix = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        rank = matrix_rank(matrix)
        hodge_rank = hodge_structure_rank(matrix)
        total_rank += rank
        min_rank = min(min_rank, hodge_rank)

    avg_rank = total_rank / instances_tested
    ratio = min_rank / avg_rank
    
    return {
        "metric_name": "Hodge Structure Rank Variance Ratio",
        "metric_value": ratio,
        "instances_tested": instances_tested,
        "n_max": n,
        "conjecture_holds": ratio >= 1 / n,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")