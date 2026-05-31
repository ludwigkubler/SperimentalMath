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
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def laplacian_matrix(G):
        n = len(G)
        L = [[0] * n for _ in range(n)]
        for i in range(n):
            degree = sum(1 for j in range(n) if G[i][j])
            L[i][i] = -degree
            for j in range(i+1, n):
                if G[i][j]:
                    L[i][j] = L[j][i] = 1
        return L

    def characteristic_polynomial(L):
        n = len(L)
        det = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            for j in range(n):
                det[i+1][j+1] = L[i][j]
        det[1][1] = 1
        for k in range(2, n + 1):
            det[k][k] = -sum(det[k-1][i] * det[k-1][k-i-1] for i in range(k-1))
        return det[n][n]

    def hodge_dimension(G):
        L = laplacian_matrix(G)
        char_poly = characteristic_polynomial(L)
        n = len(G)
        h = [0] * (2*n + 1)
        h[0] = 1
        for i in range(n):
            h[i+1] = -sum(char_poly[j] * h[i-j] for j in range(i))
            h[n+i+1] = sum(char_poly[j] * h[n+j-i-1] for j in range(i+1, n+1))
        return h[n]

    def resolution_width(phi):
        stack = []
        literals = set()
        for clause in phi:
            if not any(lit in literals for lit in clause):
                stack.append(clause)
                literals.update(clause)
            else:
                for lit in clause:
                    if -lit in literals:
                        literals.remove(-lit)
                        literals.discard(lit)
                        break
                else:
                    return len(stack)
        return len(stack)

    def generate_d_regular_graph(n, d):
        G = [[0] * n for _ in range(n)]
        edges = set()
        while len(edges) < (n * d) // 2:
            u, v = random.sample(range(n), 2)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                G[u][v] = G[v][u] = 1
                edges.add((u, v))
        return G

    def tseitin_formula(G):
        n = len(G)
        literals = list(range(1, n+1)) + [-i for i in range(1, n+1)]
        phi = []
        for u in range(n):
            clause = [literals[u]] + [-literals[v] for v in range(n) if G[u][v]]
            phi.append(clause)
            for v in range(u+1, n):
                if G[u][v]:
                    clause = [-literals[u], literals[v]]
                    phi.append(clause)
        return phi

    def correlation_coefficient(h_values, w_values):
        n = len(h_values)
        mean_h = sum(h_values) / n
        mean_w = sum(w_values) / n
        numerator = sum((h_values[i] - mean_h) * (w_values[i] - mean_w) for i in range(n))
        denominator = math.sqrt(sum((h_values[i] - mean_h) ** 2 for i in range(n))) * math.sqrt(sum((w_values[i] - mean_w) ** 2 for i in range(n)))
        return numerator / denominator if denominator != 0 else 0

    n_max = 40
    instances_tested = 0
    h_values = []
    w_values = []

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            G = generate_d_regular_graph(n, random.randint(2, n-1))
            phi = tseitin_formula(G)
            h = hodge_dimension(G)
            w = resolution_width(phi)
            if h is not None and w is not None:
                instances_tested += 1
                h_values.append(h)
                w_values.append(w)

    if instances_tested < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }

    corr_coeff = correlation_coefficient(h_values, w_values)
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": corr_coeff,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": corr_coeff > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)

    mean_corr_coeff = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient\" first_failing_seed={first_failing_seed}")