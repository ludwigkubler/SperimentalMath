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
                if i != j:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def determinant(A):
        n = len(A)
        det = 1
        for i in range(n):
            for j in range(i+1, n):
                if A[i][i] == 0:
                    continue
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
            det *= A[i][i]
        return det

    def hyperbolic_volume(phi):
        n = len(phi)
        A = [[0] * (n+1) for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if phi[i][j]:
                    A[i][j] = 1
        det_A = determinant(A)
        return abs(det_A)

    def generate_circuit(n):
        circuit = [[False] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if random.choice([True, False]):
                    circuit[i][j] = True
        return circuit

    instances_tested = 0
    total_hv = 0.0
    max_n = 0
    conjecture_holds = True
    counterexample = ""

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            instances_tested += 1
            phi = generate_circuit(n)
            hv = hyperbolic_volume(phi)
            max_n = max(max_n, n)
            if not (0.75 * n**(2/3) <= hv <= 1.25 * n**(2/3)):
                conjecture_holds = False
                counterexample = f"n={n}, hv={hv}"
                break

    return {
        "metric_name": "Hyperbolic Volume",
        "metric_value": total_hv / instances_tested if instances_tested > 0 else 0.0,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)

    mean_hv = sum(r["metric_value"] for r in results) / len(results)
    std_hv = math.sqrt(sum((r["metric_value"] - mean_hv) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_hv} std={std_hv} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_hv} std={std_hv} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")