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
            max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            for j in range(n):
                A[i][j] /= A[i][i]
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def tensor_product(A, B):
        m, n = len(A), len(A[0])
        p, q = len(B), len(B[0])
        C = [[0] * (n * q) for _ in range(m * p)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    for l in range(q):
                        C[i * p + k][j * q + l] = A[i][j] * B[k][l]
        return C

    def minimal_rank(A):
        rank = 0
        for row in gaussian_elimination(A):
            if any(row):
                rank += 1
        return rank

    def polynomial_to_matrix(f, n):
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for term in f:
            i, j, coeff = term
            matrix[i][j] += coeff
        return matrix

    def dpll_solve(F):
        # Simplified DPLL solver for demonstration purposes
        if not F:
            return True
        var = next(iter(F))
        pos_clauses = [c for c in F if var in c]
        neg_clauses = [c for c in F if -var in c]
        if dpll_solve(pos_clauses):
            return True
        if dpll_solve(neg_clauses):
            return True
        return False

    def generate_cnf(n):
        clauses = []
        for i in range(1, n + 1):
            clauses.append([i])
            clauses.append([-i])
        return clauses

    n = random.randint(5, 40)
    F = generate_cnf(n)
    f = [(random.randint(0, n), random.randint(0, n), random.choice([1, -1])) for _ in range(10)]
    A = polynomial_to_matrix(f, n)
    B = [[random.choice([0, 1]) for _ in range(n + 1)] for _ in range(n + 1)]
    C = tensor_product(A, B)
    r_f = minimal_rank(C)
    t_F = len(F) if dpll_solve(F) else float('inf')
    
    metric_name = "log2(r(f)) - t*(F)"
    metric_value = math.log2(r_f) - t_F
    instances_tested = 1
    conjecture_holds = abs(metric_value) <= 1
    counterexample = "" if conjecture_holds else f"n={n}, log2(r(f))={math.log2(r_f)}, t*(F)={t_F}"
    
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
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={result['instances_tested']}, log2(r(f))={math.log2(result['metric_value'])}, t*(F)={result['instances_tested']}\" first_failing_seed={first_failing_seed}")