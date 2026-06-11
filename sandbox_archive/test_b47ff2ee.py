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
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0 for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][k] += A[i][j] * B[j][k]
        return C

    def rank_variance(A):
        U, _, Vt = gaussian_elimination(matrix_multiplication(A, A))
        non_zero_rows = sum(1 for row in U if any(x != 0 for x in row))
        return non_zero_rows / len(U)

    def min_categorical_complexity(A):
        m, n = len(A), len(A[0])
        rank = gaussian_elimination(A)
        non_zero_columns = sum(1 for col in range(n) if any(row[col] != 0 for row in rank))
        return non_zero_columns

    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        A = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
        rank_var = rank_variance(A)
        min_cat_comp = min_categorical_complexity(A)
        results.append((rank_var, min_cat_comp))

    if len(results) < 30:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for _, n in results),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }

    rank_vars, min_cat_comps = zip(*results)
    mean_rank_var = sum(rank_vars) / len(rank_vars)
    mean_min_cat_comp = sum(min_cat_comps) / len(min_cat_comps)

    correlation = 0
    for i in range(len(results)):
        correlation += (rank_vars[i] - mean_rank_var) * (min_cat_comps[i] - mean_min_cat_comp)
    correlation /= len(results) * math.sqrt(sum((x - mean_rank_var)**2 for x in rank_vars)) * math.sqrt(sum((y - mean_min_cat_comp)**2 for y in min_cat_comps))

    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n for _, n in results),
        "conjecture_holds": correlation >= 0.8 and all(correlation >= 0.5 for _ in range(30)),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)

    mean_metric_value = sum(x["metric_value"] for x in results if x["metric_value"] is not None) / len([x for x in results if x["metric_value"] is not None])
    std_metric_value = math.sqrt(sum((x["metric_value"] - mean_metric_value)**2 for x in results if x["metric_value"] is not None)) / len([x for x in results if x["metric_value"] is not None])
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)

    if all(x["conjecture_holds"] for x in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not x["conjecture_holds"] and x["metric_value"] < 0.5 for x in results):
        first_failing_seed = next(x["seed"] for x in results if not x["conjecture_holds"] and x["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"low_correlation\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")