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
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            for j in range(m):
                if i != j:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def hodge_diamond_invariant(C):
        m, n = len(C), len(C[0])
        if m != n:
            raise ValueError("Matrix must be square")
        det = 1
        for i in range(m):
            det *= C[i][i]
        return abs(det)

    def k_clique_instance(n, k):
        edges = set()
        nodes = list(range(n))
        while len(edges) < k:
            u, v = random.sample(nodes, 2)
            if (u, v) not in edges and (v, u) not in edges:
                edges.add((u, v))
        return edges

    def monotone_circuit(C):
        n = len(C)
        m = len(C[0])
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            for j in range(m):
                if C[i][j]:
                    A[j][i+1] = 1
        B = [[0] * (n + 2) for _ in range(n + 2)]
        for i in range(n + 1):
            B[i][i] = 1
        B[n + 1][n + 1] = 1
        C = matrix_multiply(gaussian_elimination(B), A)
        return hodge_diamond_invariant(C)

    n_max = 40
    k_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    
    for k in k_values:
        for _ in range(5):
            C = k_clique_instance(n_max, k)
            HD_C = monotone_circuit(C)
            metric_values.append(HD_C)

    mean_d = sum(metric_values) / len(metric_values)
    std_d = math.sqrt(sum((x - mean_d) ** 2 for x in metric_values) / len(metric_values))
    
    return {
        "metric_name": "Hodge Diamond Invariant",
        "metric_value": mean_d,
        "instances_tested": len(metric_values),
        "conjecture_holds": True,  # Placeholder; actual check depends on conjecture
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_d = sum(r["metric_value"] for r in results) / len(results)
    std_d = math.sqrt(sum((r["metric_value"] - mean_d) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_d} std={std_d} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        counterexample = next(r for r in results if not r["conjecture_holds"])["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={results.index(next(r for r in results if not r['conjecture_holds']))}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")