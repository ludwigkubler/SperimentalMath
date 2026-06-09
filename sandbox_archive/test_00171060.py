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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + random.randint(0, m - i - 1)
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i + 1, m):
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[Fraction(0) for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][k] += A[i][j] * B[j][k]
        return C

    def rank_variance(A):
        m, n = len(A), len(A[0])
        U, S, Vt = gaussian_elimination([[Fraction(a) for a in row] for row in A]), [], []
        for i in range(m):
            if U[i][i] != 0:
                S.append(U[i][i])
        return sum((s - sum(S[:i]) / i) ** 2 for i, s in enumerate(S)) / len(S)

    def minimal_representation_length(A):
        m, n = len(A), len(A[0])
        U = gaussian_elimination([[Fraction(a) for a in row] for row in A])
        rank = sum(1 for row in U if any(row[j] != 0 for j in range(n)))
        return rank

    def pearson_correlation(X, Y):
        n = len(X)
        mean_X = sum(X) / n
        mean_Y = sum(Y) / n
        cov = sum((X[i] - mean_X) * (Y[i] - mean_Y) for i in range(n)) / n
        std_X = math.sqrt(sum((X[i] - mean_X) ** 2 for i in range(n)) / n)
        std_Y = math.sqrt(sum((Y[i] - mean_Y) ** 2 for i in range(n)) / n)
        return cov / (std_X * std_Y)

    instances_tested = 0
    rank_variances = []
    representation_lengths = []

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            A = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
            rank_variances.append(rank_variance(A))
            representation_lengths.append(minimal_representation_length(A))
            instances_tested += 1

    correlation_coefficient = pearson_correlation(rank_variances, representation_lengths)
    conjecture_holds = correlation_coefficient > Fraction(1, 3) and correlation_coefficient < Fraction(2, 3)

    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max([5, 10, 15, 20, 30, 40]),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
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
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")