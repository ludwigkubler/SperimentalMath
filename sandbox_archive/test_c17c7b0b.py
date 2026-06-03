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
        for j in range(i+1, m):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def matrix_rank(A):
    A = gaussian_elimination(A)
    rank = 0
    for row in A:
        if any(row):
            rank += 1
    return rank

def communication_matrix_rank(f, n):
    m = len(f)
    C = [[0] * (m + 1) for _ in range(m + 1)]
    for i in range(m):
        for j in range(m):
            if f[i][j]:
                C[i][j+1] += 1
                C[j][i+1] += 1
    return matrix_rank(C)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    instances_tested = 30
    total_vector_bundle_rank = 0
    total_communication_matrix_rank = 0

    for _ in range(instances_tested):
        f = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        if len(f) > 2**n:
            continue
        vector_bundle_rank = matrix_rank(f)
        communication_matrix_rank_val = communication_matrix_rank(f, n)
        total_vector_bundle_rank += vector_bundle_rank
        total_communication_matrix_rank += communication_matrix_rank_val

    mean_vector_bundle_rank = Fraction(total_vector_bundle_rank, instances_tested)
    mean_communication_matrix_rank = Fraction(total_communication_matrix_rank, instances_tested)

    if mean_communication_matrix_rank == 0:
        return {
            "metric_name": "vector_bundle_rank / communication_matrix_rank",
            "metric_value": float('inf'),
            "instances_tested": instances_tested,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "communication_matrix_rank_is_zero"
        }

    ratio = mean_vector_bundle_rank / mean_communication_matrix_rank
    correlation_coefficient = 1.0 if instances_tested == 1 else math.sqrt((instances_tested * (total_vector_bundle_rank * total_communication_matrix_rank) - sum(vector_bundle_rank * communication_matrix_rank_val for vector_bundle_rank, communication_matrix_rank_val in zip(range(instances_tested), range(instances_tested))))**2 / ((instances_tested - 1) * (sum(vector_bundle_rank**2 for vector_bundle_rank in range(instances_tested)) - instances_tested**2/instances_tested) * (sum(communication_matrix_rank_val**2 for communication_matrix_rank_val in range(instances_tested)) - instances_tested**2/instances_tested)))

    conjecture_holds = 0.5 <= ratio <= 2 and abs(correlation_coefficient) >= 0.7
    counterexample = "" if conjecture_holds else "ratio_out_of_bounds"

    return {
        "metric_name": "vector_bundle_rank / communication_matrix_rank",
        "metric_value": float(ratio),
        "instances_tested": instances_tested,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)

    mean_metric_value = sum(r['metric_value'] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r['metric_value'] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)

    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"ratio_out_of_bounds\" first_failing_seed={first_failing_seed}")