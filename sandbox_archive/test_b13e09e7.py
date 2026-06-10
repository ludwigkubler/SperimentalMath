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
            max_row = i + random.randint(0, m - i - 1)
            A[i], A[max_row] = A[max_row], A[i]
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

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B[0]), len(B)
        C = [[0 for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def min_geometric_arithmetical_rank(A):
        rank = 0
        while True:
            A = gaussian_elimination(A)
            if all(all(x == 0 for x in row) for row in A):
                break
            rank += 1
            A = [row[1:] for row in A]
        return rank

    def generate_random_protocol(n):
        A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        B = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        C = matrix_multiply(A, B)
        return A, B, C

    n_max = 40
    instances_tested = 30
    ratios = []

    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        A, B, C = generate_random_protocol(n)
        rank_variance = sum(sum(row) for row in A) * sum(sum(row) for row in B)
        mgar_r = min_geometric_arithmetical_rank(C)
        if rank_variance == 0:
            continue
        ratios.append(mgar_r / rank_variance)

    if not ratios:
        return {
            "metric_name": "mgar(r)/r",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    mean_ratio = sum(ratios) / len(ratios)
    std_ratio = math.sqrt(sum((x - mean_ratio) ** 2 for x in ratios) / len(ratios))
    
    return {
        "metric_name": "mgar(r)/r",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": all(x <= 1 for x in ratios),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")

    mean_ratio = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_ratio = math.sqrt(sum((result["metric_value"] - mean_ratio) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(result["conjecture_holds"] for result in results if result["metric_value"] is not None) / len(results)

    if all(result["conjecture_holds"] for result in results if result["metric_value"] is not None):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results if result["metric_value"] is not None):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")