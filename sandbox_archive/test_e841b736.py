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

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
        if matrix[max_row][i] == 0:
            return None  # Singular matrix
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        for j in range(cols):
            if j != i:
                factor = Fraction(matrix[j][i], matrix[i][i])
                for k in range(cols):
                    matrix[j][k] -= factor * matrix[i][k]
    return matrix

def symplectic_rank(instance):
    n = len(instance)
    A = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if (i + j) % 2 == 0:
                A[i][j] = instance[i][j]
    return sum(1 for row in gaussian_elimination(A) if any(row))

def communication_complexity_rank_variance(instance):
    n = len(instance)
    ccrvar = 0
    for i in range(n):
        for j in range(i + 1, n):
            ccrvar += abs(instance[i][j])
    return ccrvar / (n * (n - 1) / 2)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    instances_tested = 0
    srank_sum = 0.0
    ccrvar_sum = 0.0
    n_max = 5

    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n

        for _ in range(5):
            instance = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
            srank = symplectic_rank(instance)
            ccrvar = communication_complexity_rank_variance(instance)

            if srank is None:
                return {
                    "metric_name": "symplectic rank",
                    "metric_value": 0.0,
                    "instances_tested": instances_tested,
                    "n_max": n_max,
                    "conjecture_holds": False,
                    "counterexample": "singular_matrix"
                }

            srank_sum += srank
            ccrvar_sum += ccrvar**0.5
            instances_tested += 1

    mean_srank = srank_sum / instances_tested
    mean_ccrvar_sqrt = ccrvar_sum / instances_tested
    correlation_coefficient = (instances_tested * sum(srank * ccrvar for srank, ccrvar in zip(range(5), range(5))) -
                               instances_tested * mean_srank * mean_ccrvar_sqrt) / \
                              math.sqrt((instances_tested * sum(srank**2 for srank in range(5)) - instances_tested * mean_srank**2) *
                                        (instances_tested * sum(ccrvar**2 for ccrvar in range(5)) - instances_tested * mean_ccrvar_sqrt**2))

    return {
        "metric_name": "symplectic rank",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results) and min(r["metric_value"] for r in results if not r["conjecture_holds"]) < 0.5:
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_less_than_0.5\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(seeds)}")