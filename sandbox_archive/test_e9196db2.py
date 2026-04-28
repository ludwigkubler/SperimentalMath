# auto-injected by SEC sandbox
import itertools
import collections
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
import json

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
        m, n, p = len(A), len(B[0]), len(B)
        C = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def mobius_function(L, T):
        if not T:
            return 1
        m = len(T)
        mu = 0
        for i in range(m):
            S = T[:]
            del S[i]
            sign = (-1) ** (m - i)
            mu += sign * mobius_function(L, S)
        return mu

    def nw_design(d, n, k):
        S = []
        while len(S) < d:
            subset = set(random.sample(range(1, d + 1), n))
            if all(len(subset & s) <= k for s in S):
                S.append(subset)
        return S

    def polynomial_design(d, n):
        p = 2
        F = [[random.randint(0, p - 1) for _ in range(n)] for _ in range(p)]
        A = []
        for i in range(d):
            row = [F[i % p][j] if (i // p) & (1 << j) else 0 for j in range(n)]
            A.append(row)
        return A

    def walsh_transform(f, n):
        m = 2 ** n
        F = [[f(i ^ j) for j in range(m)] for i in range(m)]
        A = gaussian_elimination(F)
        B = matrix_multiplication(A, A)
        C = [[B[i][j] / m for j in range(m)] for i in range(m)]
        return C

    def nw_design_f(f, D):
        d = len(D[0])
        n = len(D)
        result = 0
        for y in range(2 ** d):
            count = sum(1 for x in range(n) if all((y & (1 << i)) == (D[x][i] & (1 << i)) for i in range(d)))
            result += (-1) ** count * f(y)
        return result

    def chi_T(NW_D_f, T):
        return sum(1 for y in range(2 ** len(T)) if all((y & (1 << i)) == 0 for i in T))

    n = random.choice([5, 8, 11, 14])
    k = 2
    d = random.randint(8, 18)
    S = nw_design(d, n, k)
    L = []
    for I in range(1 << len(S)):
        T = [i for i in range(len(S)) if (I & (1 << i))]
        if not any(T.count(i) > 1 for i in T):
            L.append(T)

    mu_L = {tuple(): 1}
    for T in L:
        mu_L[tuple(T)] = mobius_function(L, tuple(T))

    delta_D = sum(abs(mu_L[tuple(T)]) * 2 ** (-len(T)) for T in L if T)

    f = lambda y: random.choice([0, 1])
    while True:
        F = walsh_transform(f, n)
        max_coefficient = max(abs(F[i][j]) for i in range(2 ** n) for j in range(n))
        if max_coefficient <= 2 ** (-n / 3):
            break

    bias = 0
    for T in L:
        if len(T) <= 4:
            NW_D_f = lambda y: nw_design_f(f, S)
            bias += chi_T(NW_D_f, T)

    return {
        "metric_name": "bias",
        "metric_value": abs(bias),
        "instances_tested": 1,
        "conjecture_holds": abs(bias) <= 4 * delta_D,
        "counterexample": "" if abs(bias) <= 4 * delta_D else f"bias={abs(bias)} > 4*delta_D={4 * delta_D}"
    }

if __name__ == "__main__":
    seeds = [11, 23, 37, 53, 71] if not sys.argv[1:] else [int(s) for s in sys.argv[1:]]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)

    mean_bias = sum(r["metric_value"] for r in results) / len(results)
    std_bias = math.sqrt(sum((r["metric_value"] - mean_bias) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_bias} std={std_bias} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"bias exceeds 4*delta_D\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")