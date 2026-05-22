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
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            for j in range(m):
                if j != i:
                    factor = A[j][i]
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

    def ac0_circuit_size(n):
        # Placeholder function to simulate AC0 circuit size
        return n

    def tropicalization(A):
        m, n = len(A), len(A[0])
        T = [[math.inf] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if A[i][j] != 0:
                    T[i][j] = math.log(abs(A[i][j]))
        return T

    def minimal_rank(T):
        m, n = len(T), len(T[0])
        rank = 0
        for i in range(m):
            row = [T[i][j] if j < n else 0 for j in range(n)]
            if any(row[j] != math.inf for j in range(n)):
                rank += 1
        return rank

    def exponential_bound(c, n):
        return 2 ** c * n

    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        A = [[random.uniform(-10, 10) for _ in range(n)] for _ in range(n)]
        circuit_size = ac0_circuit_size(n)
        T = tropicalization(A)
        rank = minimal_rank(T)
        bound = exponential_bound(random.uniform(1, 2), n)
        results.append({"rank": rank, "circuit_size": circuit_size, "bound": bound})

    mean_rank = sum(result["rank"] for result in results) / len(results)
    mean_bound = sum(result["bound"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["rank"] > result["bound"]) / len(results)

    return {
        "metric_name": "Minimal Rank of Tropicalized Modular Form",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"mean_rank={mean_rank} <= mean_bound={mean_bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=NA support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean_rank <= mean_bound\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")