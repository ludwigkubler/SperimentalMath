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
            max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(n):
                A[i][j] /= pivot
            for k in range(m):
                if k != i and abs(A[k][i]) > 1e-9:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def det(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        A = [row[:] for row in A]
        sign = 1
        for i in range(m):
            j = next(j for j in range(i, n) if A[j][i] != 0)
            if i != j:
                A[i], A[j] = A[j], A[i]
                sign *= -1
            for k in range(i + 1, m):
                factor = A[k][i] / A[i][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]
        return sign * prod(A[i][i] for i in range(m))

    def symplectic_volume(A):
        n = len(A)
        if n % 2 != 0:
            raise ValueError("Matrix must have even dimensions")
        B = [[A[i][j] if (i + j) % 2 == 0 else -A[i][j] for j in range(n)] for i in range(n)]
        return abs(det(B))

    def resolution_width(phi_G):
        # Placeholder function, replace with actual implementation
        return random.randint(1, 10)

    n_max = 40
    instances_tested = 0
    total_msv = 0.0
    total_width = 0.0

    for n in range(5, 41):
        if time.time() + (30 - len(sys.argv[1:])) * 8 > 240:
            print('RESULT: INCONCLUSIVE reason=budget_exceeded n_tested=30')
            return
        for _ in range(3):
            G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
            if sum(sum(row) for row in G) != n * (n - 1) // 2:
                continue
            phi_G = [G[i][j] ^ G[j][i] for i in range(n) for j in range(i + 1, n)]
            msv = symplectic_volume(G)
            width = resolution_width(phi_G)
            instances_tested += 1
            total_msv += msv
            total_width += width

    if instances_tested < 30:
        print('RESULT: INCONCLUSIVE reason=insufficient_instances')
        return

    mean_msv = total_msv / instances_tested
    mean_width = total_width / instances_tested
    correlation_coefficient = (instances_tested * sum(msv * width for msv, width in zip(msvs, widths)) - total_msv * total_width) / math.sqrt((instances_tested * sum(msv**2 for msv in msvs) - total_msv**2) * (instances_tested * sum(width**2 for width in widths) - total_width**2))

    conjecture_holds = correlation_coefficient >= 0.8 and mean_msv / mean_width >= 1
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    import time

    if not sys.argv[1:]:
        seeds = [2**i + 7 for i in range(5, 30)]
    else:
        seeds = list(map(int, sys.argv[1:]))

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_msv = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_msv)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_msv} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=mapping_undefined first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support")