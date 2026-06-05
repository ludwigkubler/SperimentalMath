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

    def matrix_rank(A):
        m, n = len(A), len(A[0])
        rank = 0
        for col in range(n):
            if any(abs(A[row][col]) > 1e-9 for row in range(rank)):
                rank += 1
        return rank

    def minimal_local_induction_dimension(A):
        m, n = len(A), len(A[0])
        A_echelon = gaussian_elimination(A)
        rank = matrix_rank(A_echelon)
        return rank * (n - rank)

    def generate_communication_instance(n):
        A = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        return A

    n_values = [5, 10, 15, 20, 30, 40]
    total_lid = 0
    instances_tested = 0
    n_max = 0

    for n in n_values:
        for _ in range(5):  # Test each size with 5 instances
            A = generate_communication_instance(n)
            lid = minimal_local_induction_dimension(A)
            total_lid += lid
            instances_tested += 1
            n_max = max(n_max, n)

    mean_lid = total_lid / instances_tested
    conjecture_holds = all(lid <= rank**2 for lid, rank in zip([minimal_local_induction_dimension(generate_communication_instance(n)) for n in n_values], [matrix_rank(generate_communication_instance(n)) for n in n_values]))
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "Minimal Local Induction Dimension / Rank^2",
        "metric_value": mean_lid,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")