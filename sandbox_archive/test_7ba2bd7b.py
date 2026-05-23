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
            for j in range(i + 1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(i, n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i and A[j][i] != 0:
                    factor = A[j][i]
                    for k in range(i, n):
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

    def find_minimal_rank(M, n):
        q = len(M)
        P = [[0] * n for _ in range(n)]
        for i in range(1, n):
            P[0][i - 1] = 1
            P[i][0] = 1
        A = matrix_multiplication(P, M)
        rank = 0
        while A:
            if any(row) and all(x == 0 for row in A):
                break
            gaussian_elimination(A)
            rank += 1
            A = [row[1:] for row in A]
        return rank

    def monotone_circuit_depth(n, k):
        # Simplified approximation of the monotone circuit depth for k-CLIQUE
        return n * math.log2(k)

    n = random.randint(5, 40)
    q = random.randint(2, 10)
    M = [[random.randint(0, q - 1) for _ in range(n)] for _ in range(n)]
    minimal_rank = find_minimal_rank(M, n)
    depth = monotone_circuit_depth(n, k)

    return {
        "metric_name": "Ratio of Monotone Circuit Depth to Minimal Rank",
        "metric_value": Fraction(depth, minimal_rank),
        "instances_tested": 1,
        "conjecture_holds": depth <= 1.5 * minimal_rank,
        "counterexample": "" if depth <= 1.5 * minimal_rank else f"Ratio {depth} > 1.5"
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
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio {results[first_failing_seed]['metric_value']} > 1.5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")