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

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def construct_quantum_state(f_n, n):
        G_f = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1):
                G_f[i][j] = f_n[i ^ j]
                G_f[j][i] = G_f[i][j]
        return G_f

    def minimal_geometric_entanglement(G_f, n):
        I = [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]
        A = matrix_multiply(G_f, I)
        U, _, Vt = gaussian_elimination(A)
        entanglement = sum(sum(abs(x)) for x in U) * sum(sum(abs(x)) for x in Vt)
        return entanglement

    def communication_complexity_rank(f_n, n):
        # Placeholder function; replace with actual implementation
        return len(f_n)

    n_values = [5, 10, 15, 20, 30, 40]
    metric_value = 0.0
    instances_tested = 0
    n_max = 0

    for n in n_values:
        f_n = [random.random() for _ in range(2**n)]
        G_f = construct_quantum_state(f_n, n)
        entanglement = minimal_geometric_entanglement(G_f, n)
        rank = communication_complexity_rank(f_n, n)

        metric_value += entanglement
        instances_tested += 1
        if n > n_max:
            n_max = n

    mean_entanglement = Fraction(metric_value, instances_tested)
    conjecture_holds = all(mean_entanglement <= C * math.log(n) ** 2 for n in n_values)

    return {
        "metric_name": "Minimal Geometric Entanglement",
        "metric_value": float(mean_entanglement),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
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
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")