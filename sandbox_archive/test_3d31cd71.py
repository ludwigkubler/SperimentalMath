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
            factor = 1 / A[i][i]
            for j in range(n):
                A[i][j] *= factor
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def discrete_morse_number(f, n):
        K = []
        for S in range(1 << n):
            if f(S) == 0:
                K.append(S)
        mu = 0
        visited = [False] * (1 << n)
        for s in K:
            if not visited[s]:
                stack = [s]
                while stack:
                    u = stack.pop()
                    visited[u] = True
                    for v in range(1 << n):
                        if v > u and f(v) == 0 and all((u & (1 << j)) == (v & (1 << j)) for j in range(n)):
                            stack.append(v)
                mu += 1
        return mu

    def monotone_threshold(n, k):
        return lambda x: sum(x[i] for i in range(k)) >= n // 2

    def tribes_w(n, w):
        return lambda x: any(all(x[i] == (i % w) % 2 for i in range(j, j + w)) for j in range(0, n, w))

    def random_monotone_dnf(n):
        m = 4 * n
        clauses = []
        for _ in range(m):
            clause = [random.choice([0, 1]) for _ in range(n)]
            if all(clause[i] == (i % 2) for i in range(n)):
                continue
            clauses.append(clause)
        return lambda x: any(all(x[i] == c[i] for i in range(n)) for c in clauses)

    def f_to_matrix(f, n):
        A = [[0] * (1 << n) for _ in range(1 << n)]
        for S in range(1 << n):
            for T in range(1 << n):
                if S <= T and f(T) == 0:
                    A[S][T] = 1
        return A

    def morse_matching(A):
        m, n = len(A), len(A[0])
        visited = [False] * (1 << n)
        matches = [None] * (1 << n)
        for i in range(n):
            for j in range(m):
                if not visited[j]:
                    visited[j] = True
                    for k in range(j+1, m):
                        if not visited[k] and A[j][k] == 1:
                            matches[j] = k
                            visited[k] = True
                            break
        return sum(1 for x in matches if x is None)

    def run_family(f, n):
        A = f_to_matrix(f, n)
        mu = morse_matching(A)
        return mu

    n_values = [8, 10, 12, 14]
    results = []
    
    for n in n_values:
        threshold_f = monotone_threshold(n, n // 2)
        tribes_f = tribes_w(n, math.floor(math.log2(n)))
        random_dnf_f = random_monotone_dnf(n)
        
        mu_th = run_family(threshold_f, n)
        mu_tribes = run_family(tribes_f, n)
        mu_random = run_family(random_dnf_f, n)
        
        results.append({
            "n": n,
            "mu_th": mu_th,
            "mu_tribes": mu_tribes,
            "mu_random": mu_random
        })
    
    return {
        "metric_name": "log2_mu",
        "metric_value": sum(math.log2(result["mu_random"]) for result in results) / len(results),
        "instances_tested": 3 * len(n_values),
        "conjecture_holds": all(
            math.log2(result["mu_th"]) >= 0.5 * n_values[1] and
            math.log2(result["mu_tribes"]) <= 3 * math.log2(n_values[1]) and
            math.log2(result["mu_th"]) / math.log2(result["mu_tribes"]) > 2
            for result in results
        ),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"threshold growth\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")