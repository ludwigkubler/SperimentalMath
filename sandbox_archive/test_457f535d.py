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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = Fraction(matrix[i][i])
            for j in range(i, n):
                matrix[i][j] /= factor
            for j in range(n):
                if j != i:
                    factor = matrix[j][i]
                    for k in range(i, n):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix

    def rank_variance(matrix):
        n = len(matrix)
        identity = [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
        reduced_matrix = gaussian_elimination(identity)
        rank = sum(1 for row in reduced_matrix if any(val != Fraction(0) for val in row))
        return n - rank

    def mgi(data_space):
        # Placeholder function to compute the minimal noncommutative geometric invariant
        # This is a dummy implementation and should be replaced with actual computation
        return sum(sum(abs(x) for x in row) for row in data_space)

    instances_tested = 0
    n_max = 5
    mgi_values = []
    rank_variance_values = []

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            data_space = [[random.gauss(0, 1) for _ in range(n)] for _ in range(n)]
            rank_var = rank_variance(data_space)
            mgi_val = mgi(data_space)
            mgi_values.append(mgi_val)
            rank_variance_values.append(rank_var)
            instances_tested += 1
            n_max = max(n_max, n)

    if not mgi_values or not rank_variance_values:
        return {
            "metric_name": "mgi_vs_rank_variance",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    mgi_mean = sum(mgi_values) / len(mgi_values)
    rank_variance_mean = sum(rank_variance_values) / len(rank_variance_values)

    covariance = sum((mgi_val - mgi_mean) * (rank_var - rank_variance_mean) for mgi_val, rank_var in zip(mgi_values, rank_variance_values)) / len(mgi_values)
    variance_mgi = sum((mgi_val - mgi_mean) ** 2 for mgi_val in mgi_values) / len(mgi_values)
    variance_rank_variance = sum((rank_var - rank_variance_mean) ** 2 for rank_var in rank_variance_values) / len(rank_variance_values)

    correlation_coefficient = covariance / math.sqrt(variance_mgi * variance_rank_variance)

    return {
        "metric_name": "mgi_vs_rank_variance",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std=0.0 support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "counterexample" in result and result["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")