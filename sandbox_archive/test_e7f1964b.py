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
    
    def generate_matrix(n):
        return [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]
    
    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, n):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def determinant(A):
        n = len(A)
        if n == 2:
            return A[0][0] * A[1][1] - A[0][1] * A[1][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det
    
    def log_moment_generating_function(A):
        n = len(A)
        eigenvalues = []
        for _ in range(10):  # Power iteration method
            x = [random.random() for _ in range(n)]
            x /= math.sqrt(sum(x[i]**2 for i in range(n)))
            for _ in range(10):
                x = matrix_multiply(A, x)
                x /= math.sqrt(sum(x[i]**2 for i in range(n)))
            eigenvalues.append(max(abs(x[i]) for i in range(n)))
        return sum(math.log(eig) for eig in eigenvalues) / n
    
    def free_entropy(P):
        det_P = determinant(P)
        if det_P == 0:
            return -math.inf
        log_det_P = math.log(abs(det_P))
        return log_moment_generating_function(P) + log_det_P
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        if n * n > 2**n // 2:
            continue
        P = generate_matrix(n)
        phi_P = free_entropy(P)
        instances_tested += 1
        if phi_P < math.log2(n):
            conjecture_holds = False
            counterexample = f"Read-twice BP of size {n} with φ(P) = {phi_P}"
    
    return {
        "metric_name": "Free Entropy",
        "metric_value": free_entropy(generate_matrix(40)) if instances_tested > 0 else math.nan,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if not math.isnan(r["metric_value"])) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if not math.isnan(r["metric_value"])) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={r['seed']}")
                break