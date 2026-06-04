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

def generate_random_graph(n):
    edges = set()
    for i in range(n):
        for j in range(i + 1, n):
            if random.choice([True, False]):
                edges.add((i, j))
    return edges

def adjacency_matrix(edges, n):
    A = [[0] * n for _ in range(n)]
    for u, v in edges:
        A[u][v] = 1
        A[v][u] = 1
    return A

def transpose(A):
    n = len(A)
    T = [[A[j][i] for j in range(n)] for i in range(n)]
    return T

def multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def add(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = A[i][j] + B[i][j]
    return C

def subtract(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = A[i][j] - B[i][j]
    return C

def identity_matrix(n):
    I = [[0] * n for _ in range(n)]
    for i in range(n):
        I[i][i] = 1
    return I

def gaussian_elimination(A, b):
    n = len(A)
    M = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = max(range(i, n), key=lambda j: abs(M[j][i]))
        M[i], M[max_row] = M[max_row], M[i]
        factor = Fraction(M[i][i])
        for j in range(i, n + 1):
            M[i][j] /= factor
        for j in range(n):
            if i != j:
                factor = Fraction(M[j][i])
                for k in range(i, n + 1):
                    M[j][k] -= factor * M[i][k]
    return [row[-1] for row in M]

def determinant(A):
    n = len(A)
    if n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    det = Fraction(0)
    sign = 1
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += sign * A[0][j] * determinant(submatrix)
        sign *= -1
    return det

def minimal_local_indeterminacy(edges, n):
    A = adjacency_matrix(edges, n)
    T = transpose(A)
    AT = multiply(A, T)
    I = identity_matrix(n)
    M = subtract(AT, I)
    det_M = determinant(M)
    if det_M == 0:
        return float('inf')
    mli = Fraction(1, det_M)
    return mli

def communication_complexity_rank(edges, n):
    A = adjacency_matrix(edges, n)
    T = transpose(A)
    AT = multiply(A, T)
    I = identity_matrix(n)
    M = subtract(AT, I)
    rank = 0
    for i in range(n):
        if any(row[i] != 0 for row in M):
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    ratios = []
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):  # Aim for at least 30 instances per seed
            edges = generate_random_graph(n)
            mli = minimal_local_indeterminacy(edges, n)
            if mli == float('inf'):
                continue
            ccr = communication_complexity_rank(edges, n)
            ratio = Fraction(ccr, mli ** 2)  # Polynomial estimate: mli^2 for simplicity
            ratios.append(ratio)
            instances_tested += 1
            n_max = max(n_max, n)
    
    mean_ratio = sum(ratios) / len(ratios)
    std_deviation = math.sqrt(sum((x - mean_ratio) ** 2 for x in ratios) / len(ratios))
    support_fraction = len([r for r in ratios if r <= 1.5]) / len(ratios)
    
    conjecture_holds = support_fraction >= 0.9 and p_value < 0.05
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "communication_complexity_rank_ratio",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
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
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_deviation = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_deviation} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")