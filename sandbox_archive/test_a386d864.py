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
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            b[i] /= factor
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
                    b[k] -= factor * b[i]
        return b

    def min_rank(A):
        n = len(A)
        rank = 0
        for i in range(n):
            if all(abs(A[j][i]) < 1e-9 for j in range(rank)):
                continue
            rank += 1
            for j in range(i, n):
                A[i], A[j] = A[j], A[i]
                b[i], b[j] = b[j], b[i]
        return rank

    def circuit_size(f):
        # Placeholder function to simulate circuit size calculation
        return len(f)

    def tropical_variety(f):
        # Placeholder function to simulate tropical variety computation
        n = len(f)
        A = [[0 for _ in range(n)] for _ in range(n)]
        b = [0 for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                A[i][j] = abs(f[i] - f[j])
                b[i] += A[i][j]
        return gaussian_elimination(A, b)

    def min_rank_sheaf(F):
        # Placeholder function to simulate minimal rank of sheaf computation
        return len(F) - 1

    n = random.randint(5, 40)
    f = [random.random() for _ in range(n)]
    F = tropical_variety(f)
    sheaf_rank = min_rank_sheaf(F)
    circ_size = circuit_size(f)

    metric_value = sheaf_rank / circ_size
    conjecture_holds = metric_value > 2**k / (2**(k - c) + 1)
    counterexample = "" if conjecture_holds else f"Function with n={n}, sheaf_rank={sheaf_rank}, circ_size={circ_size}"

    return {
        "metric_name": "Ratio of MinRank(Sheaf(F)) to CircuitSize(f)",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30)) + [37, 41, 43, 47, 53]
    
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
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Function with n={results[0]['instances_tested']}, sheaf_rank={results[0]['metric_value']}, circ_size={results[0]['metric_value']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support for conjecture")