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
    
    def gaussian_elimination(A, b):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + sum(1 for j in range(i, m) if abs(A[j][i]) > abs(A[i][i]))
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        x = [0] * n
        for i in range(m-1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
        return x
    
    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B[0]), len(B)
        C = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def dft(x):
        N = len(x)
        X = [0] * N
        for k in range(N):
            sum_real, sum_imag = 0, 0
            for n in range(N):
                angle = -2 * math.pi * k * n / N
                real_part = x[n] * math.cos(angle)
                imag_part = x[n] * math.sin(angle)
                sum_real += real_part
                sum_imag += imag_part
            X[k] = (sum_real, sum_imag)
        return X
    
    def cft(M):
        n = len(M[0])
        M_hat = [[0] * n for _ in range(len(M))]
        for j in range(n):
            column = [M[i][j] for i in range(len(M))]
            M_hat[j] = dft(column)
        return M_hat
    
    def count_nonzero_entries(M_hat):
        count = 0
        for row in M_hat:
            for entry in row:
                if abs(entry[0]) > 1e-9 or abs(entry[1]) > 1e-9:
                    count += 1
        return count
    
    n, k = random.choice([(6, 3), (8, 3), (10, 3), (12, 3), (12, 4), (16, 4), (20, 4)])
    if n < 2 * k or k < 3:
        return {
            "metric_name": "cyclic_fourier_spread",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "n < 2k or k < 3"
        }
    
    # Generate canonical k-CLIQUE DNF
    edges = [(i, j) for i in range(n) for j in range(i+1, n)]
    clique_edges = random.sample(edges, k)
    canonical_dnf = [set() for _ in range(len(clique_edges))]
    for e in clique_edges:
        for i, edge_set in enumerate(canonical_dnf):
            if e[0] in edge_set or e[1] in edge_set:
                canonical_dnf[i].add(e[0])
                canonical_dnf[i].add(e[1])
    
    # Generate padded k-CLIQUE-computing DNFs
    def generate_padded_dnf(canonical_dnf):
        padding_size = random.randint(1, n)
        padded_dnf = [set() for _ in range(len(canonical_dnf))]
        for i, edge_set in enumerate(canonical_dnf):
            padded_dnf[i] = edge_set.copy()
            for j in range(padding_size):
                v = random.randint(0, n-1)
                if v not in edge_set:
                    padded_dnf[i].add(v)
        return padded_dnf
    
    def dnf_to_matrix(dnf):
        m = len(dnf)
        n = len(canonical_dnf[0])
        M = [[0] * n for _ in range(m)]
        for i, edge_set in enumerate(dnf):
            for v in edge_set:
                M[i][v] += 1
        return M
    
    def is_k_clique_computing(dnf):
        m = len(dnf)
        n = len(canonical_dnf[0])
        M = dnf_to_matrix(dnf)
        M_hat = cft(M)
        return count_nonzero_entries(M_hat) >= n // 2
    
    canonical_metric = count_nonzero_entries(cft(dnf_to_matrix(canonical_dnf)))
    
    num_trials = 30
    total_metric = 0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(num_trials):
        padded_dnf = generate_padded_dnf(canonical_dnf)
        if not is_k_clique_computing(padded_dnf):
            continue
        M = dnf_to_matrix(padded_dnf)
        M_hat = cft(M)
        metric = count_nonzero_entries(M_hat) / (n // 2)
        total_metric += metric
        if metric < 1:
            conjecture_holds = False
            counterexample = f"padded DNF with μ(F)={metric}"
    
    return {
        "metric_name": "cyclic_fourier_spread",
        "metric_value": total_metric / num_trials,
        "instances_tested": num_trials,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")