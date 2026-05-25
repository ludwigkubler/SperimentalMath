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

    def noncommutative_Lp_measure(M, p):
        m, n = len(M), len(M[0])
        if p == 1:
            return sum(abs(x) for row in M for x in row)
        elif p == float('inf'):
            return max(sum(abs(x) for x in row) for row in M)
        else:
            norm = sum(sum(abs(x)**p for x in row) for row in M)
            return norm**(1/p)

    def communication_complexity(n):
        # Simplified model of communication complexity for DISJOINTNESS
        return n * (n - 1) // 2

    n_values = [5, 10, 15, 20, 30, 40]
    measures = []
    comm_complexity = []

    for n in n_values:
        M = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        M = gaussian_elimination(M)
        measure = noncommutative_Lp_measure(M, p=2)
        measures.append(measure)
        comm_complexity.append(communication_complexity(n))

    if len(measures) != len(comm_complexity):
        return {
            "metric_name": "noncommutative_Lp_measure",
            "metric_value": 0,
            "instances_tested": len(measures),
            "conjecture_holds": False,
            "counterexample": "length_mismatch"
        }

    correlation = sum((measures[i] - mean_measures) * (comm_complexity[i] - mean_comm_complexity)
                      for i in range(len(measures))) / len(measures)

    mean_measures = sum(measures) / len(measures)
    mean_comm_complexity = sum(comm_complexity) / len(comm_complexity)

    return {
        "metric_name": "noncommutative_Lp_measure",
        "metric_value": correlation,
        "instances_tested": len(measures),
        "conjecture_holds": abs(correlation) >= 0.7,
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

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='correlation_threshold' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")