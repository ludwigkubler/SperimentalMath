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
            if A[i][i] == 0:
                continue
            factor = 1 / A[i][i]
            for j in range(n):
                A[i][j] *= factor
            for j in range(m):
                if j != i and A[j][i] != 0:
                    factor = -A[j][i]
                    for k in range(n):
                        A[j][k] += factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        if m == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det

    def hodge_index(P):
        n = len(P)
        if n == 1:
            return 0
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                A[i][j] = sum(1 for k in range(n) if (P[i] & P[j]) & (1 << k))
                A[j][i] = A[i][j]
        U = gaussian_elimination(A)
        det_U = determinant(U)
        return -math.log2(abs(det_U))

    def generate_communication_complexity_instance(n):
        variables = [1 << i for i in range(n)]
        P = set()
        for subset in range(1, 1 << n):
            if bin(subset).count('1') % 2 == 0:
                P.add(subset)
        return P

    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_hodge_index = 0
    max_n = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):
            P = generate_communication_complexity_instance(n)
            h_P = hodge_index(P)
            instances_tested += 1
            total_hodge_index += h_P
            max_n = max(max_n, n)

            if conjecture_holds and h_P > c * math.log2(n) ** 2:
                conjecture_holds = False
                counterexample = f"Hodge index {h_P} exceeds bound {c * math.log2(n) ** 2} for n={n}"

    mean_hodge_index = total_hodge_index / instances_tested if instances_tested > 0 else 0

    return {
        "metric_name": "Hodge Index",
        "metric_value": mean_hodge_index,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["counterexample"] != "" for r in results):
        counterexample = next(r["counterexample"] for r in results if r["counterexample"] != "")
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")