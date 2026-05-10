# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def run_trial(seed: int) -> dict:
    n = 40
    random.seed(seed)
    
    def generate_disjointness_matrix(n):
        M = [[0] * n for _ in range(n)]
        pairs = list(combinations(range(n), 2))
        for i, j in random.sample(pairs, min(len(pairs), n // 2)):
            M[i][j] = M[j][i] = 1
        return M
    
    def matrix_multiplication(A, B):
        m, k, n = len(A), len(B[0]), len(B)
        C = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for l in range(k):
                    C[i][j] += A[i][l] * B[l][j]
        return C
    
    def transpose(A):
        m, n = len(A), len(A[0])
        T = [[0] * m for _ in range(n)]
        for i in range(m):
            for j in range(n):
                T[j][i] = A[i][j]
        return T
    
    def svd(M):
        U = M
        V = transpose(U)
        S = [sum(x**2 for x in row) ** 0.5 for row in U]
        return U, S, V
    
    def frobenius_norm(M):
        m, n = len(M), len(M[0])
        norm = 0
        for i in range(m):
            for j in range(n):
                norm += M[i][j] ** 2
        return norm ** 0.5
    
    M = generate_disjointness_matrix(n)
    frob_norm = frobenius_norm(M)
    rank = sum(1 for s in svd(M)[1] if abs(s) > 1e-6)
    
    metric_name = "Frobenius Norm"
    metric_value = frob_norm
    instances_tested = 1
    conjecture_holds = frob_norm >= 0.9 * math.sqrt(n)
    counterexample = "" if conjecture_holds else f"Frobenius norm {frob_norm} < 0.9√{n}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Frobenius norm < 0.9√n\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")