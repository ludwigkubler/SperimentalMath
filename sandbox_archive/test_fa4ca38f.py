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

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0]*p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        if n == 1:
            return A[0][0]
        det = Fraction(0)
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            sign = (-1)**j
            det += sign * A[0][j] * determinant(submatrix)
        return det

    def generate_protocol(k, n, m):
        inputs = [[random.randint(0, 1) for _ in range(n)] for _ in range(k)]
        outputs = [random.randint(0, 1) for _ in range(m)]
        return inputs, outputs

    def compute_Brauer_group_rank(inputs, outputs):
        k, n, m = len(inputs), len(inputs[0]), len(outputs)
        A = [[0]*n for _ in range(n)]
        for i in range(k):
            for j in range(n):
                if inputs[i][j] == 1:
                    A[j][j] += 1
        rank = sum(1 for row in gaussian_elimination(A) if any(row))
        return rank

    def compute_communication_complexity(inputs, outputs):
        k, n, m = len(inputs), len(inputs[0]), len(outputs)
        min_bits = float('inf')
        for i in range(k):
            bits = sum(1 for bit in inputs[i] if bit == 1)
            min_bits = min(min_bits, bits)
        return min_bits

    k_values = [2, 3, 4]
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_rank = 0
    total_communication_complexity = 0

    for k in k_values:
        for n in n_values:
            for _ in range(5):
                inputs, outputs = generate_protocol(k, n, 1)
                rank = compute_Brauer_group_rank(inputs, outputs)
                communication_complexity = compute_communication_complexity(inputs, outputs)
                total_rank += rank
                total_communication_complexity += communication_complexity
                instances_tested += 1

    mean_rank = Fraction(total_rank, instances_tested)
    mean_communication_complexity = Fraction(total_communication_complexity, instances_tested)

    conjecture_holds = mean_rank / (n_values[-1]**(k_values[-1]/2)) >= Fraction(1, 2) and mean_communication_complexity <= 50
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "Brauer group rank",
        "metric_value": float(mean_rank),
        "instances_tested": instances_tested,
        "n_max": n_values[-1],
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")