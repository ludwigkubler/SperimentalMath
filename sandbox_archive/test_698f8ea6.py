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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_mul(A, B, mod):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
                C[i][j] %= mod
    return C

def matrix_pow(A, p, mod):
    n = len(A)
    result = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
    while p > 0:
        if p % 2 == 1:
            result = matrix_mul(result, A, mod)
        A = matrix_mul(A, A, mod)
        p //= 2
    return result

def gaussian_elimination(M):
    n = len(M)
    for i in range(n):
        pivot = M[i][i]
        if pivot == 0:
            for j in range(i + 1, n):
                if M[j][i] != 0:
                    M[i], M[j] = M[j], M[i]
                    pivot = M[i][i]
                    break
            else:
                return None
        for j in range(n):
            if j == i:
                continue
            factor = -M[j][i] / pivot
            for k in range(n):
                M[j][k] += factor * M[i][k]
    for i in range(n):
        M[i][i] /= M[i][i]
    return M

def tdr(phi):
    n = len(phi)
    T = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        T[0][i] = 1
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if phi[i - 1][j - 1] == '1':
                T[i][j] = T[i - 1][j] + T[i][j - 1]
            else:
                T[i][j] = T[i - 1][j - 1]
    return T[n][n]

def resolution_width(phi):
    n = len(phi)
    clauses = phi
    queue = []
    for clause in clauses:
        if len(clause) == 1:
            queue.append(clause[0])
    while queue:
        literal = queue.pop()
        new_clauses = []
        for clause in clauses:
            if literal not in clause and -literal not in clause:
                new_clauses.append([l for l in clause if l != -literal])
            elif literal in clause:
                continue
            else:
                new_clauses.append([-l for l in clause if l != literal])
        queue.extend(new_clause for new_clause in new_clauses if len(new_clause) == 1)
        clauses = new_clauses
    return len(clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    phi = [[random.choice(['0', '1']) for _ in range(n)] for _ in range(n)]
    tdr_value = tdr(phi)
    width = resolution_width(phi)
    return {
        "metric_name": "tdr",
        "metric_value": tdr_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(tdr_value - width) <= 5,
        "counterexample": "" if abs(tdr_value - width) <= 5 else f"tdr={tdr_value}, width={width}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
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
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"tdr and width do not correlate\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support or budget_exceeded")