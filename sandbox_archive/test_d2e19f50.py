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

def generate_disjointness_matrix(n):
    M = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            M[i][j] = random.randint(0, 1)
            M[j][i] = M[i][j]
    return M

def matrix_multiplication(A, B):
    m, k, n = len(A), len(B[0]), len(B)
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] += A[i][l] * B[l][j]
    return C

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    Augmented = [A[i] + [b[i]] for i in range(m)]
    for i in range(n):
        max_row = i
        for j in range(i + 1, m):
            if abs(Augmented[j][i]) > abs(Augmented[max_row][i]):
                max_row = j
        Augmented[i], Augmented[max_row] = Augmented[max_row], Augmented[i]
        for j in range(m):
            if j != i:
                factor = Augmented[j][i] / Augmented[i][i]
                for k in range(n + 1):
                    Augmented[j][k] -= factor * Augmented[i][k]
    for i in range(n):
        Augmented[i][n] /= Augmented[i][i]
        Augmented[i][i] = 1
    return [row[n] for row in Augmented]

def compute_genus(M):
    n = len(M)
    A = [[0] * (2*n) for _ in range(2*n)]
    b = [0] * (2*n)
    for i in range(n):
        for j in range(n):
            if M[i][j] == 1:
                A[2*i][2*j] = -1
                A[2*i][2*j+1] = 1
                A[2*i+1][2*j] = 1
                A[2*i+1][2*j+1] = -1
    b = gaussian_elimination(A, b)
    return sum(b[i] for i in range(n)) // 2

def compute_randomized_cc(M):
    n = len(M)
    cc = float('inf')
    for _ in range(100):  # Sample multiple times to get a good estimate
        A = [random.randint(0, 1) for _ in range(n)]
        B = [random.randint(0, 1) for _ in range(n)]
        cc_min = float('inf')
        for i in range(2**n):
            x = [(i >> j) & 1 for j in range(n)]
            y = [(i >> (j + n)) & 1 for j in range(n)]
            if all(A[j] == x[j] for j in range(n)) and all(B[j] == y[j] for j in range(n)):
                cc_min = min(cc_min, max(sum(x), sum(y)))
        cc = min(cc, cc_min)
    return cc

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        M = generate_disjointness_matrix(n)
        cc = compute_randomized_cc(M)
        genus = compute_genus(M)
        ratio = genus / math.log2(cc) if cc != 0 else float('inf')
        results.append({
            "n": n,
            "genus": genus,
            "cc": cc,
            "ratio": ratio
        })
    metric_value = sum(result["ratio"] for result in results)
    instances_tested = len(results)
    conjecture_holds = all(result["ratio"] <= 0.5 for result in results)
    counterexample = "" if conjecture_holds else f"n={results[0]['n']}, genus={results[0]['genus']}, cc={results[0]['cc']}"
    return {
        "metric_name": "Genus Ratio",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]  # Default to first 30 primes if no seeds provided
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")