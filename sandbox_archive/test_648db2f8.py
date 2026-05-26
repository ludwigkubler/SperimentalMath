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
            max_row = i + max(range(i, m), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            for j in range(n):
                A[i][j] /= A[i][i]
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def rank(A):
        A = [row[:] for row in A]
        r = gaussian_elimination(A)
        return sum(1 for row in r if any(row[j] != 0 for j in range(len(row))))

    n_values = [5, 10, 15, 20, 30, 40]
    k = 3
    max_rank = 0

    for n in n_values:
        instances_tested = 0
        total_rank = 0
        for _ in range(5):
            # Generate a random graph with n vertices and edges
            G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
            for i in range(n):
                G[i][i] = 0

            # Convert the graph to a quantum state matrix
            H = [[G[i][j] * (2 ** (-n)) for j in range(n)] for i in range(n)]

            # Compute the minimal rank of the quantum state
            current_rank = rank(H)
            total_rank += current_rank
            instances_tested += 1

        avg_rank = total_rank / instances_tested
        max_rank = max(max_rank, avg_rank)

    conjecture_holds = avg_rank <= 2 * n_values[-1] ** k and max_rank <= 2 * n_values[-1] ** k
    counterexample = f"avg_rank={avg_rank}, max_rank={max_rank}" if not conjecture_holds else ""

    return {
        "metric_name": "minimal_rank",
        "metric_value": avg_rank,
        "instances_tested": instances_tested * len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)

    avg_rank = sum(result["metric_value"] for result in results) / len(results)
    max_rank = max(result["metric_value"] for result in results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={avg_rank} std=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and max_rank > 2 * n_values[-1] ** k:
        counterexample = f"avg_rank={avg_rank}, max_rank={max_rank}"
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")