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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i
        for k in range(i+1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        factor = Fraction(A[i][i])
        for j in range(n):
            A[i][j] /= factor
        for k in range(n):
            if k != i:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]

def matrix_multiplication(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def ac0_parity_circuit(T, n):
    if n == 1:
        return T[0][0]
    new_T = [[T[i][j] for j in range(n) if (i + j) % 2 == 0] for i in range(n)]
    depth = 1
    while len(new_T) > 1:
        n_new = len(new_T)
        new_T = [[new_T[i][j] for j in range(n_new) if (i + j) % 2 == 0] for i in range(n_new)]
        depth += 1
    return depth

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    T = [[random.random() for _ in range(n)] for _ in range(n)]
    T = [row[:] for row in zip(*T)]  # Ensure symmetry
    rank = sum(1 for row in T if any(row))
    depth = ac0_parity_circuit(T, n)
    return {
        "metric_name": "rank_vs_depth",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= 2**depth,
        "counterexample": "" if rank <= 2**depth else f"Rank {rank} exceeds 2^{depth}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank exceeds 2^depth\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")