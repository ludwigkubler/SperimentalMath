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

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def tropicalization(A):
        m, n = len(A), len(A[0])
        T = [[-math.inf] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if A[i][j] != 0:
                    T[i][j] = math.log(abs(A[i][j]))
        return T

    def minimal_index(T):
        m, n = len(T), len(T[0])
        A = [[T[i][j] if i == j else -math.inf for j in range(n)] for i in range(m)]
        A = gaussian_elimination(A)
        min_index = 0
        for row in A:
            max_val = -math.inf
            for val in row:
                if val != -math.inf and val > max_val:
                    max_val = val
            min_index += max_val
        return min_index

    def communication_complexity_rank(n):
        # Placeholder function to simulate communication complexity rank
        return random.randint(1, n)

    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested = 0
        total_minimal_index = 0
        total_communication_complexity_rank = 0
        for _ in range(30):
            A = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
            T = tropicalization(A)
            minimal_idx = minimal_index(T)
            comm_rank = communication_complexity_rank(n)
            total_minimal_index += minimal_idx
            total_communication_complexity_rank += comm_rank
            instances_tested += 1

        mean_minimal_index = total_minimal_index / instances_tested
        mean_communication_complexity_rank = total_communication_complexity_rank / instances_tested
        pearson_corr = (instances_tested * sum(minimal_idx * comm_rank for minimal_idx, comm_rank in zip(range(1, n+1), range(1, n+1))) -
                        sum(range(1, n+1)) * sum(range(1, n+1))) / math.sqrt((instances_tested * sum(minimal_idx**2 for minimal_idx in range(1, n+1)) - sum(range(1, n+1))**2) *
                                                                 (instances_tested * sum(comm_rank**2 for comm_rank in range(1, n+1)) - sum(range(1, n+1))**2))
        mean_abs_diff = abs(mean_minimal_index - mean_communication_complexity_rank)

        results.append({
            "metric_name": "minimal_index",
            "metric_value": pearson_corr,
            "instances_tested": instances_tested,
            "n_max": n,
            "conjecture_holds": pearson_corr >= 0.8 and mean_abs_diff <= 3,
            "counterexample": "" if pearson_corr >= 0.8 and mean_abs_diff <= 3 else f"pearson_corr={pearson_corr}, mean_abs_diff={mean_abs_diff}"
        })

    return {
        "metric_name": "minimal_index",
        "metric_value": sum(r["metric_value"] for r in results) / len(results),
        "instances_tested": sum(r["instances_tested"] for r in results),
        "n_max": max(r["n_max"] for r in results),
        "conjecture_holds": all(r["conjecture_holds"] for r in results),
        "counterexample": "" if all(r["conjecture_holds"] for r in results) else next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = [run_trial(seed) for seed in seeds]

    print("TRIALS:")
    for r in results:
        print(f"TRIAL: {r}")

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if not r['conjecture_holds'])}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")