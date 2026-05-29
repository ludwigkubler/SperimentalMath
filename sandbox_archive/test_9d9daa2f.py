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
                return None
            for j in range(n):
                if j != i:
                    factor = -A[j][i] / A[i][i]
                    for k in range(i, n):
                        A[j][k] += factor * A[i][k]
        return A

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def inverse(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        I = [[Fraction(1, 1) if i == j else Fraction(0, 1) for j in range(n)] for i in range(m)]
        augmented_matrix = [A[i] + I[i] for i in range(n)]
        gaussian_elimination(augmented_matrix)
        return [row[n:] for row in augmented_matrix]

    def maslov_tft(h, n):
        h = list(h) + list(h)
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                A[i][j] = Fraction(-1, 5) * math.log(sum(math.exp(-5 * (h[(i + k) % n] + h[(j - k) % n])) for k in range(n)))
        return [abs(A[j][k]) for j in range(n) for k in range(n) if j != k]

    def mfc(h):
        return min(abs(x) for x in maslov_tft(h, len(h)))

    def delta(g, f, n):
        return abs(mfc(g) - 2 * mfc(f))

    def cv(f, n):
        deltas = []
        for _ in range(50):
            sigma = random.sample(range(n), n)
            g = [min(f[(sigma[y] + (x - y) % n)] for y in range(n)) for x in range(n)]
            deltas.append(delta(g, f, n))
        mean_delta = sum(deltas) / len(deltas)
        std_delta = math.sqrt(sum((d - mean_delta) ** 2 for d in deltas) / len(deltas))
        return std_delta / max(mean_delta, Fraction(1, 10**6))

    instances_tested = 7 * 50
    n_max = 40
    conjecture_holds = True
    counterexample = ""

    for n in [8, 12, 16, 20, 24, 32, 40]:
        f = [random.random() for _ in range(n)]
        cv_value = cv(f, n)
        if cv_value > Fraction(1, 4):
            conjecture_holds = False
            counterexample = f"n={n}, CV={cv_value}"

    return {
        "metric_name": "CV",
        "metric_value": cv_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")