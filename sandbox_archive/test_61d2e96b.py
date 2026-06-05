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
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_rank(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(m):
            if any(A[i]):
                rank += 1
        return rank

    def minimal_local_induction_dimension(A):
        m, n = len(A), len(A[0])
        A_augmented = [row + [1] for row in A]
        A_rref = gaussian_elimination(A_augmented)
        free_vars = n - sum(1 for row in A_rref if any(row))
        return free_vars

    def generate_communication_matrix(rank):
        matrix = []
        while len(matrix) < rank:
            row = [random.choice([0, 1]) for _ in range(rank)]
            if row not in matrix:
                matrix.append(row)
        return matrix

    n_max = 40
    instances_tested = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            R = random.randint(1, min(n, 10))
            comm_matrix = generate_communication_matrix(R)
            lid = minimal_local_induction_dimension(comm_matrix)
            instances_tested += 1
            total_metric_value += lid / (R ** 2)

    mean_metric_value = total_metric_value / instances_tested
    if any(lid / (R ** 2) > 1 for R, lid in zip([5, 10, 15, 20, 30, 40], [minimal_local_induction_dimension(generate_communication_matrix(R)) for R in [5, 10, 15, 20, 30, 40]])):
        conjecture_holds = False
        counterexample = "LID/R^2 > 1 for some rank"

    return {
        "metric_name": "LID/R^2",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["counterexample"] == "LID/R^2 > 1 for some rank" for r in results):
        print(f"RESULT: FALSIFIED counterexample=\"LID/R^2 > 1 for some rank\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")