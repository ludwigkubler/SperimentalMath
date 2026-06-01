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
            max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            denom = A[i][i]
            for j in range(n):
                A[i][j] /= denom
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B[0]), len(B)
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
        det = Fraction(0)
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det

    def tropicalization(phi):
        n = len(phi)
        T = [[-math.inf] * n for _ in range(n)]
        for i, clause in enumerate(phi):
            for var in clause:
                if var >= 0:
                    T[var][i] = max(T[var][i], -i)
                else:
                    T[-var - 1][i] = max(T[-var - 1][i], -i)
        return T

    def frege_proof_depth(phi):
        stack = []
        for clause in phi:
            if all(var < 0 or var not in [x[1] for x in stack] for var in clause):
                stack.append((len(clause), random.choice(clause)))
        return len(stack)

    def min_local_ring_unit_group_size(T):
        m, n = len(T), len(T[0])
        A = [[-math.inf] * (n + 1) for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if T[i][j] != -math.inf:
                    A[i][j] = max(A[i][j], T[i][j])
                    A[j][i] = max(A[j][i], T[i][j])
        A[m][m] = 0
        for k in range(m):
            for i in range(m):
                for j in range(m):
                    if A[i][k] != -math.inf and A[k][j] != -math.inf:
                        A[i][j] = max(A[i][j], A[i][k] + A[k][j])
        return int(-A[m][m])

    n_max = 40
    instances_tested = 0
    correlation_coefficient = Fraction(0)
    p_value = Fraction(1)

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            phi = [[random.randint(-n, n - 1) for _ in range(random.randint(1, n))] for _ in range(n)]
            T = tropicalization(phi)
            mu_phi = min_local_ring_unit_group_size(T)
            d_phi = frege_proof_depth(phi)
            instances_tested += 1
            if mu_phi != -math.inf and d_phi != math.inf:
                correlation_coefficient += Fraction(mu_phi * d_phi, n_max ** 2)
                p_value *= Fraction(1, n_max)

    correlation_coefficient /= instances_tested
    p_value = 1 - (1 - p_value) ** instances_tested

    conjecture_holds = correlation_coefficient >= Fraction(7, 10) and p_value < Fraction(5, 100)
    counterexample = "mapping_undefined" if not conjecture_holds else ""

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": float(correlation_coefficient),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = [run_trial(seed) for seed in seeds]

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
    
    print(f"RESULT: {'SUPPORTED' if support_fraction >= 0.8 else 'FALSIFIED'} mean={mean_value} std={std_value} support_fraction={support_fraction}")