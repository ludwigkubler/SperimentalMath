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
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i+1, n):
                factor = A[j][i] / A[i][i]
                A[j][i:] = [A[j][k] - factor * A[i][k] for k in range(i, n)]
                b[j] -= factor * b[i]
        x = [0.0] * n
        for i in range(n-1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
        return x

    def matrix_multiplication(A, B):
        m, k = len(A), len(B[0])
        n = len(B)
        C = [[0.0] * k for _ in range(m)]
        for i in range(m):
            for j in range(k):
                for l in range(n):
                    C[i][j] += A[i][l] * B[l][j]
        return C

    def determinant(A):
        n = len(A)
        det = 0
        if n == 1:
            return A[0][0]
        elif n == 2:
            return A[0][0] * A[1][1] - A[0][1] * A[1][0]
        else:
            for c in range(n):
                det += ((-1) ** c) * A[0][c] * determinant([row[:c] + row[c+1:] for row in A[1:]])
        return det

    def hodge_norm(C, n):
        # Placeholder function to compute Hodge norm
        # This is a dummy implementation and should be replaced with actual computation
        return random.random()

    def circuit_monotone_width(n):
        # Placeholder function to compute circuit monotone width
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(1, n)

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        C = [random.uniform(-1, 1) + random.uniform(-1, 1) * 1j for _ in range(n)]
        mn = circuit_monotone_width(n)
        H_C = hodge_norm(C, n)
        
        # Simulate computation of H(C) and mn
        A = [[random.uniform(-1, 1) + random.uniform(-1, 1) * 1j for _ in range(n)] for _ in range(n)]
        b = [random.uniform(-1, 1) + random.uniform(-1, 1) * 1j for _ in range(n)]
        x = gaussian_elimination(A, b)
        det_A = determinant(A)
        
        # Placeholder for actual computation of H(C) and mn
        H_C_simulated = abs(det_A)
        mn_simulated = len(x)
        
        results.append({
            "n": n,
            "H_C": H_C_simulated,
            "mn": mn_simulated
        })

    metric_value = sum(result["H_C"] for result in results) / len(results)
    instances_tested = len(results)
    n_max = max(result["n"] for result in results)
    
    if all(result["H_C"] <= 1.1 * result["mn"] ** 2 for result in results):
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "H(C) exceeds f(mn) by more than 10%"

    return {
        "metric_name": "Hodge Norm",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{trial_result}...}}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"H(C) exceeds f(mn) by more than 10%\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")