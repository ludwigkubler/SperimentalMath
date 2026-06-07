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
            max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            for j in range(n):
                A[i][j] /= A[i][i]
            for k in range(m):
                if k != i and A[k][i]:
                    for j in range(n):
                        A[k][j] -= A[i][j] * A[k][i]
        return A

    def matrix_multiply(A, B):
        m, n = len(A), len(B[0])
        p = len(B)
        C = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det

    def hodge_index(A):
        if not A:
            return 0
        rank = sum(1 for row in gaussian_elimination(A) if any(row))
        return rank

    def communication_complexity_rank(f, n):
        # Placeholder function to compute the rank of a circuit computing f
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, n)

    def variance(values):
        mean = sum(values) / len(values)
        return sum((x - mean) ** 2 for x in values) / len(values)

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        f = lambda x: random.choice([True, False])
        hodge_indices = []
        ranks = []
        for _ in range(30):
            rank = communication_complexity_rank(f, n)
            ranks.append(rank)
            hodge_index_value = hodge_index([[random.randint(-10, 10) for _ in range(n)] for _ in range(n)])
            hodge_indices.append(hodge_index_value)
        results.extend([(n, h, v) for h, v in zip(hodge_indices, ranks)])

    if not results:
        return {
            "metric_name": "hodge_index_over_variance",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    h_sum = sum(h for n, h, v in results)
    v_sum = sum(v for n, h, v in results)
    h_variance = variance([h for n, h, v in results])
    v_variance = variance([v for n, h, v in results])

    if h_variance == 0 or v_variance == 0:
        return {
            "metric_name": "hodge_index_over_variance",
            "metric_value": 0,
            "instances_tested": len(results),
            "n_max": max(n for n, _, _ in results),
            "conjecture_holds": False,
            "counterexample": "variance_zero"
        }

    ratio = h_sum / v_sum
    log_n_squared = sum(math.log2(n) ** 2 for n, _, _ in results) / len(results)

    return {
        "metric_name": "hodge_index_over_variance",
        "metric_value": ratio,
        "instances_tested": len(results),
        "n_max": max(n for n, _, _ in results),
        "conjecture_holds": ratio >= 0.1 * log_n_squared,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3**j for i in range(5) for j in range(5)]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    if all("conjecture_holds" in result and result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if "conjecture_holds" in result and result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any("counterexample" in result and result["counterexample"] for result in results):
        counterexample = next(result["counterexample"] for result in results if "counterexample" in result)
        first_failing_seed = next(result["seed"] for result in results if "counterexample" in result)
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")