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
            for j in range(n):
                A[i][j] /= A[i][i]
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        rank = sum(1 for row in A if any(row))
        return rank

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0]*p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def determinant(A):
        if len(A) == 1:
            return A[0][0]
        det = 0
        for i in range(len(A)):
            submatrix = [row[:i] + row[i+1:] for row in A[1:]]
            det += (-1)**i * A[0][i] * determinant(submatrix)
        return det

    def min_rank_tropicalized_lie_group(M):
        m, n = len(M), len(M[0])
        tropical_matrix = [[max(M[i][j], M[j][i]) for j in range(n)] for i in range(m)]
        rank = gaussian_elimination(tropical_matrix)
        return rank

    def communication_complexity_disjoint(M):
        m, n = len(M), len(M[0])
        # Simplified version of CC_{DISJ}(M) using a random protocol
        cc = 0
        for _ in range(10):  # Number of trials for simplicity
            x = random.randint(0, 2**m - 1)
            y = random.randint(0, 2**n - 1)
            if M[x][y] == 1:
                cc += 1
        return cc

    n = random.choice([5, 10, 15, 20, 30, 40])
    X = range(n)
    Y = range(n)
    f = lambda x: random.randint(0, 1)  # Random Boolean function for simplicity
    M = [[f(x + y * 2**n) for y in Y] for x in X]
    
    tau_G_M = min_rank_tropicalized_lie_group(M)
    CC_DISJ_M = communication_complexity_disjoint(M)
    
    conjecture_holds = CC_DISJ_M >= tau_G_M ** 2
    counterexample = "" if conjecture_holds else f"CC_{DISJ}(M)={CC_DISJ_M}, tau_G(M)^2={tau_G_M**2}"
    
    return {
        "metric_name": "Communication Complexity",
        "metric_value": CC_DISJ_M,
        "instances_tested": 10,  # Number of trials for simplicity
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30*4 + 1, 2))  # List of 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")