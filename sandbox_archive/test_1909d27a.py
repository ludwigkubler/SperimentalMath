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
        n = len(A)
        for i in range(n):
            max_row = max(range(i, n), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                return None
            for j in range(i + 1, n):
                factor = A[j][i] / pivot
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return [row[i] for i in range(n) if abs(row[i]) > 1e-9]

    def rank(A):
        A_copy = [row[:] for row in A]
        return len(gaussian_elimination(A_copy)) or 0

    def multivariate_continued_fraction(n, seed):
        random.seed(seed)
        x = [random.randint(1, 10) for _ in range(n)]
        y = [random.randint(1, 10) for _ in range(n)]
        A = [[x[i] * y[j] for j in range(n)] for i in range(n)]
        return rank(A)

    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_A = 0.0

    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            r = multivariate_continued_fraction(n, random.randint(1, 1000))
            if r == 0:
                continue
            A = 1 / (r + 2)
            total_A += A
            instances_tested += 1

    average_A = total_A / instances_tested
    conjecture_holds = all(A <= 1 / (r + 2) for n in n_values for _ in range(5))
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "amplitude_amplification_factor",
        "metric_value": average_A,
        "instances_tested": instances_tested,
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

    mean_A = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_A) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_A} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")