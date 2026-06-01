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
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
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

    def minimal_symplectic_volume(A):
        U = gaussian_elimination(A)
        volume = 1
        for i in range(len(U)):
            if U[i][i] != 0:
                volume *= abs(U[i][i])
        return volume

    def resolution_proof_width(phi):
        # Placeholder function to simulate resolution proof width calculation
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, 10)

    n_values = [5, 10, 15, 20, 30, 40]
    min_vols = []
    widths = []

    for n in n_values:
        phi = [random.choice([1, -1]) * random.randint(1, n) for _ in range(n)]
        A = [[phi[i] * phi[j] if i == j else 0 for j in range(n)] for i in range(n)]
        min_vol = minimal_symplectic_volume(A)
        width = resolution_proof_width(phi)

        min_vols.append(min_vol)
        widths.append(width)

    correlation_coefficient = sum((min_vols[i] - mean_min_vols) * (widths[i] - mean_widths) for i in range(len(n_values))) / len(n_values)
    slope = correlation_coefficient * (mean_widths / mean_min_vols)

    conjecture_holds = correlation_coefficient >= 0.8 and abs(slope) <= 2
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")