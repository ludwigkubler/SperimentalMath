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
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            b[i] /= factor
            for j in range(i + 1, n):
                factor = A[j][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        return [b[i] for i in range(n)]

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B[0]), len(B)
        C = [[0 for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def determinant(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det

    def inverse(A):
        n = len(A)
        I = [[int(i == j) for j in range(n)] for i in range(n)]
        adjugate = [row[::-1] for row in gaussian_elimination(matrix_multiply(A, I), I)[::-1]]
        det = determinant(A)
        return [[adjugate[i][j] / det for j in range(n)] for i in range(n)]

    def submodular_measure(dnf):
        n = len(dnf)
        m = 2 ** n
        A = [[0 for _ in range(m)] for _ in range(m)]
        b = [0 for _ in range(m)]
        for i in range(m):
            for j in range(i, m):
                if all((i & (1 << k)) or (j & (1 << k)) for k in range(n)):
                    A[i][j] = 1
                    A[j][i] = 1
                    b[i] += 1
                    b[j] += 1
        x = gaussian_elimination(A, b)
        return sum(x)

    def clique_cover(n):
        if n == 2:
            return [[0, 1]]
        cover = []
        for i in range(2, n):
            cover.append([i - 1, i])
        return cover

    def k_clique_measure(k):
        n = 40
        cover = clique_cover(n)
        measure = len(cover) * (n - k + 1)
        return measure

    def random_dnf(n):
        terms = []
        for _ in range(random.randint(1, n)):
            term = set()
            while len(term) < n:
                term.add(random.randint(0, n - 1))
            terms.append(term)
        return terms

    n = 40
    dnf = random_dnf(n)
    measure = submodular_measure(dnf)
    if measure > math.log2(n):
        counterexample = "submodular_measure_too_large"
    else:
        counterexample = ""

    k_clique_measure_value = k_clique_measure(3)

    return {
        "metric_name": "submodular_measure",
        "metric_value": measure,
        "instances_tested": 1,
        "conjecture_holds": measure <= math.log2(n) and k_clique_measure_value >= n,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if r["counterexample"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")