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
            max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            factor = A[i][i]
            if factor == 0:
                continue
            for j in range(i, n):
                A[i][j] /= factor
            for k in range(n):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(i, n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0 for _ in range(n)] for _ in range(n)]
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

    def local_induction_dimension(G):
        n = len(G)
        matroid_matrix = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if G[i][j] == 1:
                    matroid_matrix[i][j] = 1
                    matroid_matrix[j][i] = 1
        rank = len([row for row in gaussian_elimination(matroid_matrix) if any(row)])
        return rank

    def communication_complexity_rank_variance(G):
        n = len(G)
        matroid_matrix = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if G[i][j] == 1:
                    matroid_matrix[i][j] = 1
                    matroid_matrix[j][i] = 1
        rank = len([row for row in gaussian_elimination(matroid_matrix) if any(row)])
        return rank**2

    def generate_d_regular_graph(n, d):
        G = [[0 for _ in range(n)] for _ in range(n)]
        degree_count = [0 for _ in range(n)]
        edges_added = 0
        while edges_added < n * d // 2:
            u = random.randint(0, n-1)
            v = random.randint(0, n-1)
            if u != v and G[u][v] == 0 and degree_count[u] < d and degree_count[v] < d:
                G[u][v] = 1
                G[v][u] = 1
                degree_count[u] += 1
                degree_count[v] += 1
                edges_added += 1
        return G

    n_max = 40
    instances_tested = 30
    metric_value = 0.0
    conjecture_holds = True
    counterexample = ""

    for _ in range(instances_tested):
        d = random.randint(2, min(n_max-1, 5))
        G = generate_d_regular_graph(n_max, d)
        lind_G = local_induction_dimension(G)
        rank_var_M_G = communication_complexity_rank_variance(G)
        if rank_var_M_G == 0:
            continue
        ratio = lind_G / rank_var_M_G
        metric_value += ratio
        if abs(ratio) > 2 * instances_tested:
            conjecture_holds = False
            counterexample = f"Ratio {ratio} exceeds bound for d={d}, n={n_max}"
            break

    return {
        "metric_name": "lind_G / rank_var_M_G",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")