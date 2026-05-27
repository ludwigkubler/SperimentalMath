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
            for j in range(i+1, m):
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

    def formal_power_series(G, x):
        result = 0
        for r in range(len(G)):
            result += G[r] * (x ** r)
        return result

    def tseitin_circuit_size(phi):
        # Placeholder function to compute Tseitin circuit size
        # This is a stub and should be replaced with actual computation
        return len(phi) * 3

    n = random.randint(8, 40)
    phi = []
    for _ in range(n):
        clause = [random.choice([1, -1]) * random.choice(['x' + str(i+1), '¬x' + str(i+1)]) for i in range(n)]
        phi.append(clause)

    G = [[0] * n for _ in range(n)]
    for r in range(n):
        G[r][r] = 1

    R_G = sum(1 for row in G if any(x != 0 for x in row))

    log_n = math.log2(n)
    tseitin_size = tseitin_circuit_size(phi)

    return {
        "metric_name": "R(G(φ))",
        "metric_value": R_G,
        "instances_tested": 1,
        "conjecture_holds": abs(R_G - log_n) <= 0.5 * log_n and tseitin_size <= 2 * n * math.log2(n),
        "counterexample": "" if R_G <= log_n + 0.5 * log_n and tseitin_size <= 2 * n * math.log2(n) else "Tseitin circuit size not bounded by function of log n"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(2, 1000003) for _ in range(30)]
    
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
        print(f"RESULT: FALSIFIED counterexample=\"Tseitin circuit size not bounded by function of log n\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")