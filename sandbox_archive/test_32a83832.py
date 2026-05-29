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
            max_row = i + max(range(i, m), key=lambda x: abs(A[x][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(n):
                if j != i:
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
    
    def fft(a, inverse=False):
        n = len(a)
        if n == 1:
            return a
        even = fft(a[0::2], inverse)
        odd = fft(a[1::2], inverse)
        T = [math.exp(-2j * math.pi * k / n) if inverse else math.exp(2j * math.pi * k / n) for k in range(n // 2)]
        return [even[k] + T[k] * odd[k] for k in range(n // 2)] + [even[k] - T[k] * odd[k] for k in range(n // 2)]
    
    def maslov_tft(f, n):
        a = [f[(i % n) + (j % n)] for i in range(n) for j in range(n)]
        a = fft(a)
        return [abs(x) for x in fft([x.real for x in a])]
    
    def mfc(h):
        h = maslov_tft(h, len(h))
        return min(abs(h[k]) for k in range(1, len(h)))
    
    def delta(g, f, n):
        return abs(mfc(g) - 2 * mfc(f))
    
    def cv(f, n):
        deltas = []
        for _ in range(50):
            sigma = random.sample(range(n), n)
            g = [min(f[sigma[y]] + f[(x - y) % n] for y in range(n)) for x in range(n)]
            deltas.append(delta(g, f, n))
        mean_delta = sum(deltas) / len(deltas)
        std_dev_delta = math.sqrt(sum((d - mean_delta) ** 2 for d in deltas) / len(deltas))
        return std_dev_delta / max(mean_delta, 1e-6)
    
    results = []
    for n in [8, 12, 16, 20, 24, 32, 40]:
        f = [random.random() for _ in range(n)]
        cv_value = cv(f, n)
        results.append({
            "n": n,
            "cv": cv_value
        })
    
    mean_cv = sum(result["cv"] for result in results) / len(results)
    std_cv = math.sqrt(sum((result["cv"] - mean_cv) ** 2 for result in results) / len(results))
    conjecture_holds = all(result["cv"] <= 0.25 for result in results)
    
    return {
        "metric_name": "orbit_coefficient_of_variation",
        "metric_value": mean_cv,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"CV > 0.25 at n={results[results.index(max(results, key=lambda x: x['cv']))]['n']}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, 'metric_name': '{result['metric_name']}', 'metric_value': {result['metric_value']}, 'instances_tested': {result['instances_tested']}, 'n_max': {result['n_max']}, 'conjecture_holds': {result['conjecture_holds']}, 'counterexample': '{result['counterexample']}'}}")
        results.append(result)
    
    mean_cv = sum(result["metric_value"] for result in results) / len(results)
    std_cv = math.sqrt(sum((result["metric_value"] - mean_cv) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_cv} std={std_cv} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and any(result["cv"] > 0.25 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"CV > 0.25\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")