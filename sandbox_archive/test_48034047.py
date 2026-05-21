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
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            for j in range(n):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def determinant(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            det += (-1)**j * A[0][j] * determinant([row[:j] + row[j+1:] for row in A[1:]])
        return det

    def geometric_entropy(T):
        n = len(T)
        entropy = 0
        for i in range(n):
            for j in range(n):
                if T[i][j] != 0:
                    entropy += -T[i][j] * math.log2(T[i][j])
        return entropy

    def k_complexity(I):
        n, m = len(I), len(I[0])
        A = [[0]*n for _ in range(n)]
        for i in range(m):
            for j in range(n):
                if I[j][i] == 1:
                    A[j][j] += 1
        det_A = determinant(A)
        return math.log2(det_A)

    def construct_tropical_curve(I):
        n, m = len(I), len(I[0])
        T = [[0]*n for _ in range(n)]
        for i in range(m):
            for j in range(n):
                if I[j][i] == 1:
                    T[j][j] += 1
        return T

    def generate_instance(n, m):
        I = [[random.randint(0, 1) for _ in range(m)] for _ in range(n)]
        return I

    n_max = 40
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            m = random.randint(1, min(2*n, n_max))
            I = generate_instance(n, m)
            T = construct_tropical_curve(I)
            H_T_I = geometric_entropy(T)
            K_I = k_complexity(I)
            results.append({
                "metric_name": "geometric_entropy",
                "metric_value": H_T_I,
                "instances_tested": 1,
                "conjecture_holds": H_T_I <= 2 * K_I,
                "counterexample": f"n={n}, m={m}, H(T_I)={H_T_I}, K(I)={K_I}" if not (H_T_I <= 2 * K_I) else ""
            })

    return {
        "metric_name": "geometric_entropy",
        "metric_value": sum(r["metric_value"] for r in results),
        "instances_tested": len(results),
        "conjecture_holds": all(r["conjecture_holds"] for r in results),
        "counterexample": next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")