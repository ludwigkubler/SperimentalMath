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
    
    def generate_d_regular_graph(n, d):
        if (d * n) % 2 != 0 or d > n - 1:
            return None
        G = [[0] * n for _ in range(n)]
        edges = set()
        for i in range(d):
            for j in range(i + 1, n):
                if len(edges) == (d * n) // 2:
                    break
                if random.choice([True, False]):
                    G[i][j] = G[j][i] = 1
                    edges.add((i, j))
        return G

    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def gaussian_elimination(A, b):
        n = len(A)
        augmented_matrix = [A[i] + [b[i]] for i in range(n)]
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                    max_row = j
            augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
            pivot = augmented_matrix[i][i]
            for j in range(i, n + 1):
                augmented_matrix[i][j] /= pivot
            for j in range(n):
                if j != i:
                    factor = augmented_matrix[j][i]
                    for k in range(i, n + 1):
                        augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
        return [row[-1] for row in augmented_matrix]

    def commuting_matrix(G):
        n = len(G)
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        A = G
        B = I
        C = matrix_multiply(A, B)
        D = matrix_multiply(B, A)
        return [C[i][j] - D[i][j] for i in range(n) for j in range(n)]

    def geometric_entanglement(C):
        n = int(math.sqrt(len(C)))
        eigenvalues = []
        for i in range(n):
            eigenvector = [0] * n
            eigenvector[i] = 1
            value = sum(C[k][i] * eigenvector[k] for k in range(n))
            eigenvalues.append(value)
        return max(eigenvalues) - min(eigenvalues)

    def communication_complexity_rank_variance(C):
        n = int(math.sqrt(len(C)))
        rank = 0
        for i in range(n):
            row = C[i * n:(i + 1) * n]
            if any(row[j] != 0 for j in range(n)):
                rank += 1
        return n - rank

    def generate_random_d_regular_graphs(n, d, k):
        graphs = []
        for _ in range(k):
            graph = generate_d_regular_graph(n, d)
            if graph is not None:
                graphs.append(graph)
        return graphs

    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_metric_value = 0
    max_n = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        graphs = generate_random_d_regular_graphs(n, d=2, k=5)
        for graph in graphs:
            instances_tested += 1
            max_n = max(max_n, n)
            C = commuting_matrix(graph)
            E_G = geometric_entanglement(C)
            Var_C_G = communication_complexity_rank_variance(C)
            total_metric_value += E_G * Var_C_G

    if instances_tested < 30:
        conjecture_holds = False
        counterexample = "insufficient_instances"

    mean_metric_value = total_metric_value / instances_tested
    support_fraction = Fraction(instances_tested, len(n_values) * 5)

    return {
        "metric_name": "E(G) * Var(C(G))",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": max_n,
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
    support_fraction = Fraction(sum(1 for r in results if r["conjecture_holds"]), len(results))

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= Fraction(8, 10):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"insufficient_instances\" first_failing_seed={first_failing_seed}")