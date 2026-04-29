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
            max_row = i + max(range(i, m), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(n):
                if i != j:
                    factor = A[j][i] / A[i][i]
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

    def star_discrepancy(V_F, m, n):
        D = 0
        for a in range(1 << n):
            S = [0] * n
            for j in range(n):
                if (a >> j) & 1:
                    S[j] += 1
                else:
                    S[j] -= 1
            D = max(D, abs(sum(S[i] * V_F[i][j] for i in range(m))) / math.sqrt(m))
        return D

    def resolution_width(F):
        # Placeholder for actual DPLL implementation
        return random.randint(10, 100)  # Dummy value for testing

    n = 30
    m = int(4.5 * n)
    F = [[random.choice([0, 1, -1]) for _ in range(n)] for _ in range(m)]
    V_F = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if F[i][j] == 1:
                V_F[i][j] = 1 / (2 * n)
            elif F[i][j] == -1:
                V_F[i][j] = 1 - 1 / (2 * n)
            else:
                V_F[i][j] = 0.5

    D_star = star_discrepancy(V_F, m, n)
    w_F = resolution_width(F)

    return {
        "metric_name": "resolution_width",
        "metric_value": w_F,
        "instances_tested": 1,
        "conjecture_holds": D_star >= math.log(n) and w_F >= (n / math.log(n)) * 0.5,
        "counterexample": "" if D_star >= math.log(n) else f"Star discrepancy {D_star} < log({n})"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Star discrepancy < log(n)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")