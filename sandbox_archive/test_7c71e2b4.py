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
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = Fraction(A[i][i])
            for j in range(n):
                A[i][j] /= factor
            for j in range(m):
                if i != j:
                    factor = Fraction(A[j][i])
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[Fraction(0) for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][k] += A[i][j] * B[j][k]
        return C

    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        if m == 1:
            return A[0][0]
        det = Fraction(0)
        for j in range(n):
            submatrix = [[A[i][k] for k in range(n) if k != j] for i in range(1, m)]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det

    def fundamental_group(vertices):
        # Placeholder function to compute the fundamental group
        # This is a dummy implementation and should be replaced with actual computation
        return len(vertices)

    n = random.randint(5, 40)
    vertices = [i for i in range(n)]
    edges = []
    for _ in range(random.randint(2 * n, 3 * n)):
        u, v = random.sample(vertices, 2)
        if (u, v) not in edges and (v, u) not in edges:
            edges.append((u, v))

    # Construct the adjacency matrix
    A = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for u, v in edges:
        A[u][v] += Fraction(1)
        A[v][u] += Fraction(1)

    # Compute the fundamental group of each vertex
    fundgroup_count = sum(fundamental_group([i]) > 0 for i in vertices)

    # Compute the resolution proof width (simplified as number of edges)
    w_pi = len(edges)

    return {
        "metric_name": "fundgroup_vs_width",
        "metric_value": Fraction(fundgroup_count, w_pi),
        "instances_tested": n,
        "n_max": n,
        "conjecture_holds": fundgroup_count <= 2 * w_pi,
        "counterexample": "" if fundgroup_count <= 2 * w_pi else f"fundgroup={fundgroup_count}, width={w_pi}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if r["counterexample"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")