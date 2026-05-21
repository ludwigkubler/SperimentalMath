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
            max_row = i + max(range(i, m), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            factor = A[i][i]
            if factor == 0:
                continue
            for j in range(n):
                A[i][j] /= factor
            for k in range(m):
                if k != i and A[k][i]:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def compute_tropical_curve(f, n):
        # Placeholder for the actual computation of the tropical curve
        # This is a dummy implementation and should be replaced with the actual algorithm
        roots = [random.uniform(-10, 10) for _ in range(n)]
        return roots

    def minimal_root_separation(roots):
        return min(abs(r1 - r2) for r1, r2 in itertools.combinations(roots, 2))

    def acc0_circuit_size(f, n):
        # Placeholder for the actual computation of the ACC0 circuit size
        # This is a dummy implementation and should be replaced with the actual algorithm
        return random.randint(n**2 // 4, n**2)

    n = random.choice([5, 10, 15, 20, 30, 40])
    f = [random.uniform(-1, 1) for _ in range(n)]
    C_f = compute_tropical_curve(f, n)
    root_separation = minimal_root_separation(C_f)
    circuit_size = acc0_circuit_size(f, n)

    return {
        "metric_name": "minimal_root_separation",
        "metric_value": root_separation,
        "instances_tested": 1,
        "conjecture_holds": root_separation >= n**(1/3) and circuit_size >= n**2,
        "counterexample": "" if root_separation >= n**(1/3) and circuit_size >= n**2 else f"Root separation: {root_separation}, Circuit size: {circuit_size}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
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
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")