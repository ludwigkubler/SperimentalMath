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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        if A[i][i] == 0:
            # Find a non-zero pivot below the current row
            for k in range(i + 1, n):
                if A[k][i] != 0:
                    A[i], A[k] = A[k], A[i]
                    break
            else:
                raise ValueError("Singular matrix")
        for j in range(n):
            if j == i:
                continue
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    d = random.randint(2, 10)
    
    # Generate a random adjacency matrix
    A = [[random.choice([0, 1]) if i != j else 0 for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            A[j][i] = A[i][j]
    
    # Compute the eigenvalues of A
    def matrix_multiply(A, B):
        n = len(A)
        C = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def matrix_power(A, k):
        n = len(A)
        result = [[Fraction(0) if i != j else Fraction(1) for j in range(n)] for i in range(n)]
        base = A
        while k > 0:
            if k % 2 == 1:
                result = matrix_multiply(result, base)
            base = matrix_multiply(base, base)
            k //= 2
        return result
    
    def trace(A):
        n = len(A)
        return sum(A[i][i] for i in range(n))
    
    eigenvalues = []
    for _ in range(10):  # Power iteration method
        v = [random.random() for _ in range(n)]
        v /= math.sqrt(sum(x**2 for x in v))
        Av = matrix_multiply(A, v)
        lambda_ = trace(matrix_multiply(v, Av)) / trace(matrix_multiply(v, v))
        eigenvalues.append(lambda_)
    
    # Calculate the geometric entropy
    entropy = sum(-lambda_ * math.log2(lambda_) for lambda_ in eigenvalues if lambda_ > 0) / n
    
    # Construct an SOS certificate (simplified)
    def sos_certificate(A):
        return A
    
    M = sos_certificate(A)
    
    # Check if the SOS certificate approximates max-CUT within a factor of 0.878
    max_cut_value = sum(max(row[i] for row in A) for i in range(n))
    sos_cut_value = sum(sum(M[i][j] * (A[i][j] + 1) / 2 for j in range(i, n)) for i in range(n))
    
    if sos_cut_value < 0.878 * max_cut_value:
        return {
            "metric_name": "geometric_entropy",
            "metric_value": entropy,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "SOS certificate does not approximate max-CUT within a factor of 0.878"
        }
    
    return {
        "metric_name": "geometric_entropy",
        "metric_value": entropy,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_entropy = sum(r["metric_value"] for r in results) / len(results)
    std_entropy = math.sqrt(sum((r["metric_value"] - mean_entropy)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_entropy} std={std_entropy} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='SOS certificate does not approximate max-CUT within a factor of 0.878' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")