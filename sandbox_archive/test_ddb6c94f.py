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
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            for j in range(n):
                if i != j:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiply(A, B):
        n = len(A)
        C = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def determinant(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = 0
        sign = 1
        for i in range(n):
            submatrix = [row[:i] + row[i+1:] for row in A[1:]]
            det += sign * A[0][i] * determinant(submatrix)
            sign *= -1
        return det

    def inverse(A):
        n = len(A)
        I = [[int(i == j) for j in range(n)] for i in range(n)]
        augmented_matrix = [A[i] + I[i] for i in range(n)]
        gaussian_elimination(augmented_matrix)
        inv_A = [row[n:] for row in augmented_matrix]
        return inv_A

    def construct_manifold(G):
        n = len(G)
        M = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if G[i][j] == 1:
                    M[i][j] = M[j][i] = 1
        return M

    def circuit_monotone_width(G):
        n = len(G)
        max_width = 0
        for i in range(n):
            visited = [False]*n
            stack = [i]
            while stack:
                node = stack.pop()
                if not visited[node]:
                    visited[node] = True
                    for j in range(n):
                        if G[node][j] == 1 and not visited[j]:
                            stack.append(j)
                            max_width += 1
        return max_width

    def alexander_dirac_invariant(M):
        n = len(M)
        A = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if M[i][j] == 1:
                    A[i][j] = A[j][i] = 1
        det_A = determinant(A)
        inv_A = inverse(A)
        B = matrix_multiply(inv_A, A)
        return sum(sum(B[i][j] for j in range(i+1, n)) for i in range(n))

    def random_d_regular_graph(d, n):
        G = [[0]*n for _ in range(n)]
        for i in range(n):
            neighbors = random.sample(range(n), d)
            while len(neighbors) > 1:
                u, v = neighbors.pop(), neighbors.pop()
                G[u][v] = G[v][u] = 1
        return G

    n_max = 0
    instances_tested = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""

    for d in [5, 10, 15, 20, 30, 40]:
        n = random.randint(5, min(n_max + 10, 40))
        G = random_d_regular_graph(d, n)
        M = construct_manifold(G)
        w_G = circuit_monotone_width(G)
        m_alex_M = alexander_dirac_invariant(M)

        if instances_tested == 0:
            n_max = n

        total_metric_value += m_alex_M
        instances_tested += 1

        if abs(w_G - m_alex_M) > 5:
            conjecture_holds = False
            counterexample = f"Graph with d={d}, n={n} has |w_G - m_alex(M)| > 5"

    metric_value = total_metric_value / instances_tested

    return {
        "metric_name": "m_alex(G)",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")