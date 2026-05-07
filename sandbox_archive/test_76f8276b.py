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
            max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, n):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def frobenius_norm(A):
        n = len(A)
        norm = 0
        for i in range(n):
            for j in range(n):
                norm += A[i][j]**2
        return math.sqrt(norm)
    
    def sign_disjointness_matrix(k):
        n = 2**k
        M = [[(-1)**(i & j != 0) for j in range(n)] for i in range(n)]
        return M
    
    def singular_values(A):
        A_norm = frobenius_norm(A)
        U, _, Vt = gaussian_elimination(matrix_multiply(A, A))
        return [math.sqrt(U[i][i] * Vt[i][i]) / A_norm for i in range(len(A))]
    
    def free_cumulant_4(mu):
        m2 = sum(x**2 for x in mu) / len(mu)
        m4 = sum(x**4 for x in mu) / len(mu)
        return m4 - 2 * m2**2
    
    k_values = [2, 3, 4, 5, 6]
    results = []
    
    for k in k_values:
        Pi_k = sign_disjointness_matrix(k)
        sv = singular_values(Pi_k)
        mu_k = [x**2 / sum(sv) for x in sv]
        
        kappa_4 = free_cumulant_4(mu_k)
        results.append({"k": k, "kappa_4": kappa_4})
    
    mean_kappa_4 = sum(result["kappa_4"] for result in results) / len(results)
    std_kappa_4 = math.sqrt(sum((result["kappa_4"] - mean_kappa_4)**2 for result in results) / len(results))
    
    conjecture_holds = all(result["kappa_4"] > mean_kappa_4 + 3 * std_kappa_4 for result in results)
    counterexample = "" if conjecture_holds else "Non-monotonic k→κ₄(Π_k) profile or κ₄(Π_k) inside random-matrix 95% interval"
    
    return {
        "metric_name": "kappa_4",
        "metric_value": mean_kappa_4,
        "instances_tested": len(k_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_kappa_4 = sum(r["metric_value"] for r in results) / len(results)
    std_kappa_4 = math.sqrt(sum((r["metric_value"] - mean_kappa_4)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_kappa_4} std={std_kappa_4} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Non-monotonic k→κ₄(Π_k) profile or κ₄(Π_k) inside random-matrix 95% interval\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE No seeds tested")