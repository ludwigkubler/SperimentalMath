# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a, m):
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("Inverse doesn't exist")
    else:
        return x % m

def matrix_multiply(A, B):
    n = len(A)
    result = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] += A[i][k] * B[k][j]
    return result

def gaussian_elimination(A, b):
    n = len(A)
    M = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(M[j][i]) > abs(M[max_row][i]):
                max_row = j
        M[i], M[max_row] = M[max_row], M[i]
        factor = Fraction(M[i][i])
        for j in range(n):
            M[i][j] /= factor
        b[i] /= factor
        for j in range(n):
            if i != j:
                factor = Fraction(M[j][i])
                for k in range(n):
                    M[j][k] -= factor * M[i][k]
                b[j] -= factor * b[i]
    return [m[-1] for m in M]

def sign_quotient_rows(f, k):
    N = 2**k
    rows = set()
    for i in range(N):
        row = []
        for j in range(k):
            if f(i >> j & 1) == 1:
                row.append(1)
            else:
                row.append(-1)
        rows.add(tuple(row))
    return list(rows)

def projective_hamming_distance(r, s):
    N = len(r)
    return min(sum(x != y for x, y in zip(r, s)), N - sum(x != y for x, y in zip(r, s)))

def union_find(n):
    parent = list(range(n))
    rank = [0] * n

    def find(i):
        if parent[i] != i:
            parent[i] = find(parent[i])
        return parent[i]

    def union(i, j):
        root_i = find(i)
        root_j = find(j)
        if root_i != root_j:
            if rank[root_i] > rank[root_j]:
                parent[root_j] = root_i
            elif rank[root_i] < rank[root_j]:
                parent[root_i] = root_j
            else:
                parent[root_j] = root_i
                rank[root_i] += 1

    return union, find

def count_components(rows):
    n = len(rows)
    uf, _ = union_find(n)
    for i in range(n):
        for j in range(i+1, n):
            if projective_hamming_distance(rows[i], rows[j]) <= 2**(len(rows[0])-2):
                uf(i, j)
    return len(set(uf(i) for i in range(n)))

def rank_R(M):
    n = len(M)
    M_int = [[int(x) for x in row] for row in M]
    det = Fraction(1)
    for i in range(n):
        pivot = None
        for j in range(i, n):
            if M[j][i] != 0:
                pivot = j
                break
        if pivot is None:
            return 0
        det *= Fraction(M[pivot][i], gcd(det.numerator, M[pivot][i]))
        for j in range(n):
            M[pivot][j] /= M[pivot][i]
        for j in range(n):
            if j != pivot:
                factor = -M[j][i]
                for k in range(n):
                    M[j][k] += factor * M[pivot][k]
    return det.numerator

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [8, 16, 32, 64]:
        k = n.bit_length() - 1
        f_types = ["IP", "EQ", "GT", "AND-of-XORs", "MAJ"]
        for f_type in f_types:
            if f_type == "IP":
                f = lambda x: x & (x >> 1)
            elif f_type == "EQ":
                f = lambda x: x & (x >> 2)
            elif f_type == "GT":
                f = lambda x: x & (x >> 3)
            elif f_type == "AND-of-XORs":
                f = lambda x: x & (x ^ (x >> 1))
            else:
                f = lambda x: int(x > n // 2)
            for r in [1, 2, 4, 8]:
                rows = sign_quotient_rows(f, k)
                M = []
                for row in rows:
                    M.append([Fraction(row[i]) for i in range(n)])
                tau_pm = count_components(rows)
                rk_R_val = rank_R(M)
                results.append((tau_pm, rk_R_val))
    tau_pm_total = sum(tau_pm for tau_pm, _ in results)
    rk_R_total = sum(rk_R_val for _, rk_R_val in results)
    mean_tau_pm = Fraction(tau_pm_total, len(results)).limit_denominator()
    std_tau_pm = (sum((tau_pm - mean_tau_pm)**2 for tau_pm, _ in results) / len(results))**0.5
    support_fraction = sum(1 for tau_pm, rk_R_val in results if tau_pm <= rk_R_val) / len(results)
    return {
        "metric_name": "tau_pm",
        "metric_value": float(mean_tau_pm),
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.99,
        "counterexample": "" if support_fraction >= 0.99 else f"support_fraction={support_fraction}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    mean_tau_pm = sum(r["metric_value"] for r in results) / len(results)
    std_tau_pm = (sum((r["metric_value"] - mean_tau_pm)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if support_fraction >= 0.99:
        print(f"RESULT: SUPPORTED mean={mean_tau_pm} std={std_tau_pm} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")