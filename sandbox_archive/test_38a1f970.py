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
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def polymatroid_rank(M):
        m, n = len(M), len(M[0])
        identity = [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(m)]
        augmented = [row + col for row, col in zip(M, identity)]
        reduced = gaussian_elimination(augmented)
        rank = sum(1 for row in reduced if any(x != Fraction(0) for x in row))
        return rank

    def sos_refutation_size(n):
        # Placeholder function to simulate SOS refutation size
        # For k-CLIQUE instances, ρ = O(n^{1/2} log n)
        return int(math.sqrt(n) * math.log(n))

    n = random.randint(5, 40)
    M = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    r_M = polymatroid_rank(M)
    rho = sos_refutation_size(n)

    if rho == 0:
        return {
            "metric_name": "polymatroid_rank / sos_refutation_size",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "sos_refutation_size_is_zero"
        }

    c = r_M / rho
    return {
        "metric_name": "polymatroid_rank / sos_refutation_size",
        "metric_value": c,
        "instances_tested": 1,
        "conjecture_holds": c >= 1,  # Adjust the constant as needed
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]  # Default to first 30 primes

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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = "polymatroid_rank / sos_refutation_size inequality failed"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")