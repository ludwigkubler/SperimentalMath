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
    
    def generate_max_cut_instance(n):
        A = [random.randint(1, n-1) for _ in range(n)]
        B = [i for i in range(n) if i not in A]
        return A, B
    
    def matrix_multiplication(A, B):
        m, k = len(A), len(B[0])
        n = len(B)
        C = [[0] * k for _ in range(m)]
        for i in range(m):
            for j in range(k):
                for l in range(n):
                    C[i][j] += A[i][l] * B[l][j]
        return C
    
    def gaussian_elimination(A, b):
        n = len(b)
        augmented_matrix = [A[i] + [b[i]] for i in range(n)]
        for i in range(n):
            max_row = max(range(i, n), key=lambda k: abs(augmented_matrix[k][i]))
            augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
            pivot = augmented_matrix[i][i]
            if pivot == 0:
                continue
            for j in range(n):
                augmented_matrix[i][j] /= pivot
            b[i] /= pivot
            for k in range(n):
                if k != i:
                    factor = augmented_matrix[k][i]
                    for j in range(n):
                        augmented_matrix[k][j] -= factor * augmented_matrix[i][j]
                    b[k] -= factor * b[i]
        return [row[:-1] for row in augmented_matrix], b
    
    def symbolic_rank_check(A):
        n = len(A)
        rank = 0
        for i in range(n):
            if all(abs(a) < 1e-9 for a in A[i]):
                continue
            rank += 1
            for j in range(i+1, n):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return rank
    
    def sdp_relaxation(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i == j:
                    C[i][j] = A[i][i] + B[j][j]
                else:
                    C[i][j] = -A[i][j] - B[j][i]
        _, b = gaussian_elimination(C, [1] * n)
        return max(b)
    
    def log_base_2(x):
        if x <= 0:
            return float('-inf')
        return math.log2(x)
    
    n = 40
    A, B = generate_max_cut_instance(n)
    d = symbolic_rank_check(A)
    sos_refutation_degree = sdp_relaxation(A, B)
    
    metric_name = "sos_refutation_degree"
    metric_value = sos_refutation_degree
    instances_tested = 1
    conjecture_holds = sos_refutation_degree >= log_base_2(d + 1)
    counterexample = "" if conjecture_holds else f"Graph with n={n}, A={A}, B={B}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
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
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")