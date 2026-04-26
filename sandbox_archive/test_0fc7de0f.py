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

    def generate_design(ℓ: int, a: int, m: int):
        M = [[0] * ℓ for _ in range(m)]
        for i in range(m):
            while True:
                S = set(random.sample(range(ℓ), a))
                if all(len(S.intersection(row)) <= 1 for row in M[:i]):
                    for j in S:
                        M[i][j] = 1
                    break
        return M

    def compute_disc(M: list):
        m, ℓ = len(M), len(M[0])
        disc = float('inf')
        for coloring in product([-1, 1], repeat=ℓ):
            row_sums = [sum(M[i][j] * coloring[j] for j in range(ℓ)) for i in range(m)]
            disc = min(disc, max(abs(sum_) for sum_ in row_sums))
        return disc

    def compute_as(f: callable):
        n = len(next(iter(f.keys())))
        as_f = 0
        for x in product([0, 1], repeat=n):
            if f[x] != f[tuple(1 - bit for bit in x)]:
                as_f += 1
        return as_f / n

    def compute_beta(D: list, f: callable):
        m, ℓ = len(D), len(D[0])
        disc = compute_disc(D)
        s = random.randint(0, 2**ℓ - 1)
        seed_coloring = [((s >> j) & 1) * 2 - 1 for j in range(ℓ)]
        output_counts = [0] * m
        for i in range(m):
            if sum(D[i][j] * seed_coloring[j] for j in range(ℓ)) >= disc:
                output_counts[i] += 1

        def evaluate_t(t: list, s: int) -> float:
            x = [((s >> j) & 1) for j in range(len(t))]
            return sum(t[i] * f[x[:i+1]] for i in range(len(t))) / (2 ** len(t))

        beta = 0
        for width in range(1, m + 1):
            for t in combinations(range(m), width):
                beta = max(beta, abs(evaluate_t(list(t), s) - evaluate_t(list(t)[::-1], s)))
        return beta

    def gaussian_elimination(A: list):
        m, n = len(A), len(A[0])
        for i in range(m):
            pivot = i
            while pivot < m and A[pivot][i] == 0:
                pivot += 1
            if pivot == m:
                continue
            A[i], A[pivot] = A[pivot], A[i]
            for j in range(n):
                if j != i:
                    factor = A[j][i] / A[i][i]
                    for k in range(i, n):
                        A[j][k] -= factor * A[i][k]

    def matrix_multiplication(A: list, B: list):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def compute_fourier(f: callable, n: int):
        fourier_coeffs = [0] * (2 ** n)
        for x in product([0, 1], repeat=n):
            fourier_coeffs[sum(x)] += f[x]
        for i in range(2 ** n):
            fourier_coeffs[i] /= 2 ** n
        return fourier_coeffs

    def product(iterable):
        result = 1
        for x in iterable:
            result *= x
        return result

    def combinations(iterable, r):
        pool = list(iterable)
        n = len(pool)
        if r > n:
            return
        indices = list(range(r))
        yield tuple(pool[i] for i in indices)
        while True:
            for i in reversed(range(r)):
                if indices[i] != i + n - r:
                    break
            else:
                return
            indices[i] += 1
            for j in range(i + 1, r):
                indices[j] = indices[j - 1] + 1
            yield tuple(pool[i] for i in indices)

    def norm_infinity(v: list):
        return max(abs(x) for x in v)

    n_values = [6, 8, 10, 12]
    a_values = [2, 3, 4]
    m_max = 2 * max(n_values)
    functions = {
        "parity": lambda x: sum(x) % 2,
        "inner_product": lambda x: sum(x[:len(x)//2]) == sum(x[len(x)//2:])
    }
    for _ in range(5):
        ℓ = random.randint(4, min(16, m_max))
        a = random.choice(a_values)
        m = random.randint(1, m_max)
        D = generate_design(ℓ, a, m)
        disc = compute_disc(D)

        for func_name in functions:
            f = functions[func_name]
            as_f = compute_as(f)
            beta = compute_beta(D, f)
            fourier_coeffs = compute_fourier(f, a)
            slope = sum(beta * (disc / m) * 2 ** as_f - fourier_coeffs[i] for i in range(1, len(fourier_coeffs))) / (len(fourier_coeffs) - 1)

            if beta > 4 * (disc / m) * 2 ** as_f + 2 ** (-a / 2):
                return {
                    "metric_name": "beta",
                    "metric_value": beta,
                    "instances_tested": 1,
                    "conjecture_holds": False,
                    "counterexample": f"Function {func_name} with a={a}, m={m}"
                }

    return {
        "metric_name": "beta",
        "metric_value": sum(beta * (disc / m) * 2 ** as_f - fourier_coeffs[i] for i in range(1, len(fourier_coeffs))) / (len(fourier_coeffs) - 1),
        "instances_tested": 5,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Function {r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")