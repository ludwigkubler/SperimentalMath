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
        return [row[:n-1] for row in A]

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def fourier_coefficients(f, n):
        N = 2 ** n
        a = [0] * N
        for x in range(N):
            for y in range(N):
                a[(x + y) % N] += f(x // (N // 2), y // (N // 2))
        return [(1 / N) * sum(a[i] * math.exp(-2j * math.pi * i * j / N) for i in range(N)) for j in range(N)]

    def additive_energy(f, n):
        a = fourier_coefficients(f, n)
        E = 0
        for i in range(len(a)):
            for j in range(i+1, len(a)):
                E += abs(a[i] * a[j])
        return E

    def sos_refutation_time(n):
        # Placeholder function to simulate SOS refutation time
        # Replace with actual implementation if available
        return 2 ** (n // 2)

    n = 10
    f = lambda x, y: (x + y) % 2  # Example Sipser-like function

    E_f = additive_energy(f, n)
    refutation_time = sos_refutation_time(n)

    metric_name = "Additive Energy"
    metric_value = E_f
    instances_tested = 1
    conjecture_holds = E_f <= n**2 and refutation_time <= 2**(n**0.5)
    counterexample = "" if conjecture_holds else f"Counterexample: E[f] = {E_f}, refutation time = {refutation_time}"

    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
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
        counterexample_desc = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")