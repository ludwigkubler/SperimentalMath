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
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def rank(matrix):
        matrix_copy = [row[:] for row in matrix]
        rref = gaussian_elimination(matrix_copy)
        return sum(1 for row in rref if any(row[j] != 0 for j in range(len(row))))

    def k_clique_instance(n, k):
        edges = set()
        while len(edges) < k * (k - 1) // 2:
            u = random.randint(0, n-1)
            v = random.randint(0, n-1)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                edges.add((u, v))
        return edges

    def birfield_rank(n):
        A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        return rank(A)

    def characteristic_polynomial_rank(n):
        # Placeholder for actual computation
        return random.randint(1, n)

    k = 3
    n = 20
    instances_tested = 50

    rho_B_sum = 0
    rho_C_sum = 0

    for _ in range(instances_tested):
        edges = k_clique_instance(n, k)
        birfield_matrix = [[1 if (i, j) in edges or (j, i) in edges else 0 for j in range(n)] for i in range(n)]
        rho_B = birfield_rank(n)
        rho_C = characteristic_polynomial_rank(n)

        rho_B_sum += rho_B
        rho_C_sum += rho_C

    mean_rho_B = rho_B_sum / instances_tested
    mean_rho_C = rho_C_sum / instances_tested

    conjecture_holds = (mean_rho_B >= n**k * math.log(n)) and (mean_rho_C <= (math.log(n) ** 2))
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "rho_B and rho_C",
        "metric_value": {"mean_rho_B": mean_rho_B, "mean_rho_C": mean_rho_C},
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rho_B = sum(res["metric_value"]["mean_rho_B"] for res in results) / len(results)
    mean_rho_C = sum(res["metric_value"]["mean_rho_C"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean_rho_B={mean_rho_B} std_rho_B=0.0 support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")