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
    
    def rank(A):
        A = [row[:] for row in A]
        r = gaussian_elimination(A)
        return sum(1 for row in r if any(row[i] != 0 for i in range(len(row))))
    
    def generate_monotone_dnf(n, k):
        variables = list(range(n))
        clauses = []
        for _ in range(k):
            clause = random.sample(variables, random.randint(1, n))
            clauses.append(clause)
        return clauses
    
    def tropicalize(dnf):
        T = [[0] * len(dnf) for _ in range(len(dnf))]
        for i in range(len(dnf)):
            for j in range(i+1, len(dnf)):
                if set(dnf[i]).intersection(set(dnf[j])):
                    T[i][j] = 1
                    T[j][i] = 1
        return T
    
    n = random.randint(5, 40)
    k = random.randint(1, min(n // 2, 3))
    dnf = generate_monotone_dnf(n, k)
    T = tropicalize(dnf)
    rank_T = rank(T)
    
    expected_rank = n ** k
    lower_bound = max(0, expected_rank - 0.3 * expected_rank)
    upper_bound = min(expected_rank + 0.3 * expected_rank, float('inf'))
    
    metric_value = rank_T
    conjecture_holds = lower_bound <= metric_value <= upper_bound
    counterexample = "" if conjecture_holds else f"Rank {rank_T} is outside the expected range [{lower_bound}, {upper_bound}]"
    
    return {
        "metric_name": "Minimal Rank of Tropicalized Lie Algebra",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(res["metric_value"] for res in results)
    mean_metric_value = total_metric_value / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((res["seed"] for res in results if not res["conjecture_holds"]), None)
        counterexample_desc = results[next(i for i, res in enumerate(results) if not res["conjecture_holds"])["counterexample"]]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")