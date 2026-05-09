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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def determinant(A):
    n = len(A)
    det = 1
    U = gaussian_elimination(A)
    for i in range(n):
        det *= U[i][i]
    return det

def log_det(M, t):
    I = [[int(i == j) for j in range(len(M))] for i in range(len(M))]
    M_t = [[M[i][j] + t * I[i][j] for j in range(len(M[0]))] for i in range(len(M))]
    return math.log(abs(determinant(M_t)))

def adaptive_quadrature(f, a, b, tol=1e-6):
    def integrate(f, a, b, n):
        h = (b - a) / n
        s = 0.5 * (f(a) + f(b))
        for i in range(1, n):
            s += f(a + i * h)
        return s * h

    n = 2
    while True:
        I_n = integrate(f, a, b, n)
        I_2n = integrate(f, a, b, 2 * n)
        error = abs(I_2n - I_n) / 3
        if error < tol:
            return I_2n
        n *= 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    M = [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]
    
    def f(t):
        return log_det(M, t)
    
    phi_M = adaptive_quadrature(f, -10, 10) / (2 * math.pi)
    instances_tested = n * n
    conjecture_holds = phi_M >= 0.8 * math.sqrt(n)
    counterexample = "" if conjecture_holds else f"phi(M)={phi_M} < 0.8√n"
    
    return {
        "metric_name": "phi(M)",
        "metric_value": phi_M,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_phi_M = sum(r["metric_value"] for r in results) / len(results)
    std_phi_M = math.sqrt(sum((r["metric_value"] - mean_phi_M)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_phi_M} std={std_phi_M} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"phi(M) < 0.8√n\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")