# auto-injected by SEC sandbox
import collections
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
import json
from fractions import Fraction

def generate_3_regular_graph(n, seed):
    random.seed(seed)
    stubs = [i // 3 for i in range(3 * n)]
    random.shuffle(stubs)
    edges = []
    for i in range(0, 3 * n, 2):
        u, v = stubs[i], stubs[i + 1]
        if u != v and (u, v) not in edges and (v, u) not in edges:
            edges.append((u, v))
    if len(edges) != n:
        return None
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj

def matrix_mult(A, B):
    n = len(A)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_add(A, B):
    n = len(A)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            result[i][j] = A[i][j] + B[i][j]
    return result

def matrix_sub(A, B):
    n = len(A)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            result[i][j] = A[i][j] - B[i][j]
    return result

def matrix_scalar_mult(A, scalar):
    n = len(A)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            result[i][j] = A[i][j] * scalar
    return result

def jacobi_rotation(A):
    n = len(A)
    V = [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
    for _ in range(100):
        max_val = Fraction(0)
        p, q = 0, 1
        for i in range(n):
            for j in range(i + 1, n):
                if abs(A[i][j]) > max_val:
                    max_val = abs(A[i][j])
                    p, q = i, j
        if max_val < Fraction(1, 10**6):
            break
        if A[p][p] == A[q][q]:
            theta = Fraction(math.pi, 4)
        else:
            theta = Fraction(1, 2) * math.atan(Fraction(2 * A[p][q], A[p][p] - A[q][q]))
        c = math.cos(theta)
        s = math.sin(theta)
        R = [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
        R[p][p] = Fraction(c)
        R[p][q] = Fraction(-s)
        R[q][p] = Fraction(s)
        R[q][q] = Fraction(c)
        A = matrix_mult(matrix_mult(R.T, A), R)
        V = matrix_mult(V, R)
    eigenvalues = [A[i][i] for i in range(n)]
    return eigenvalues, V

def compute_moments(eigenvalues):
    n = len(eigenvalues)
    m1 = sum(eigenvalues) / n
    m2 = sum(e ** 2 for e in eigenvalues) / n
    m3 = sum(e ** 3 for e in eigenvalues) / n
    m4 = sum(e ** 4 for e in eigenvalues) / n
    return m1, m2, m3, m4

def compute_free_cumulants(m1, m2, m3, m4):
    kappa2 = m2 - m1 ** 2
    kappa4 = m4 - 4 * m3 * m1 - 2 * m2 ** 2 + 10 * m2 * m1 ** 2 - 5 * m1 ** 4
    return kappa2, kappa4

def compute_max_cut(adj):
    n = len(adj)
    max_cut = 0
    for mask in range(1 << n):
        cut_size = 0
        for u in range(n):
            for v in adj[u]:
                if (mask & (1 << u)) != (mask & (1 << v)):
                    cut_size += 1
        if cut_size > max_cut:
            max_cut = cut_size
    return max_cut

def compute_sdp2(eigenvalues):
    n = len(eigenvalues)
    lambda_max = max(eigenvalues)
    sdp2 = (3 * n / 8) * (1 + lambda_max - 1)
    return sdp2

def run_trial(seed):
    n_values = [8, 10, 12, 14, 16]
    results = []
    for n in n_values:
        adj = None
        while adj is None:
            adj = generate_3_regular_graph(n, seed)
            seed += 1
        D = [[0] * n for _ in range(n)]
        for i in range(n):
            D[i][i] = len(adj[i])
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in adj[i]:
                A[i][j] = 1
        L_hat = matrix_scalar_mult(matrix_sub(D, A), Fraction(1, 3))
        eigenvalues, _ = jacobi_rotation(L_hat)
        m1, m2, m3, m4 = compute_moments(eigenvalues)
        kappa2, kappa4 = compute_free_cumulants(m1, m2, m3, m4)
        max_cut = compute_max_cut(adj)
        sdp2 = compute_sdp2(eigenvalues)
        g = sdp2 / max_cut
        epsilon = max(0, kappa4 / (kappa2 ** 2) - 1) if kappa2 != 0 else 0
        T = (g - 1) * math.log2(n) - 4 * (epsilon + 1 / n)
        results.append({
            "n": n,
            "T": float(T),
            "g": float(g),
            "epsilon": float(epsilon),
            "max_cut": max_cut,
            "sdp2": float(sdp2),
            "eigenvalues": [float(e) for e in eigenvalues]
        })
    metric_value = sum(r["T"] for r in results) / len(results)
    conjecture_holds = all(r["T"] <= 0 for r in results)
    counterexample = ""
    if not conjecture_holds:
        for r in results:
            if r["T"] > 0:
                counterexample = f"n={r['n']}, T={r['T']}, g={r['g']}, epsilon={r['epsilon']}, max_cut={r['max_cut']}, sdp2={r['sdp2']}, eigenvalues={r['eigenvalues']}"
                break
    return {
        "metric_name": "T",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    trials = []
    for seed in seeds:
        result = run_trial(seed)
        trials.append(result)
        print(f"TRIAL: {json.dumps({'seed': seed, **result})}")
    metric_values = [trial["metric_value"] for trial in trials]
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(trial["conjecture_holds"] for trial in trials) / len(trials)
    if all(trial["conjecture_holds"] for trial in trials):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        for trial in trials:
            if not trial["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{trial['counterexample']}\" first_failing_seed={seeds[trials.index(trial)]}")
                break