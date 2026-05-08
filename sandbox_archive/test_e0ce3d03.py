# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import deque

def matrix_add(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def matrix_sub(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def matrix_mul(A, B):
    result = [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
    return result

def identity_matrix(n):
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]

def trace(matrix):
    return sum(matrix[i][i] for i in range(len(matrix)))

def frobenius_norm(matrix):
    return math.sqrt(sum(sum(abs(x) ** 2 for x in row) for row in matrix))

def is_nilpotent(matrix, tolerance=1e-9):
    n = len(matrix)
    identity = identity_matrix(n)
    current = matrix
    for c in range(1, n + 1):
        if frobenius_norm(current) < tolerance:
            return c - 1
        current = matrix_mul(current, matrix_sub(matrix_add(*matrix_bar_k), identity))
    return float('inf')

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def build_bp(n):
        layers = []
        for _ in range(2 * n):
            states = [random.randint(0, 1) for _ in range(2 ** (n + 1))]
            transition_matrix = [[states[i] ^ states[j] for j in range(2 ** (n + 1))] for i in range(2 ** (n + 1))]
            layers.append((transition_matrix, random.choice([0, 1])))
        return layers
    
    def extract_M_bar_k(layers):
        M_bar_k = []
        s = len(layers[0][0])
        for layer, parity in layers:
            M_k = matrix_add(*[matrix_mul(layer, layer) if p == parity else identity_matrix(s) for p in range(2)])
            M_bar_k.append(matrix_sub(M_k, [[trace(M_k) / s] * s for _ in range(s)]))
        return M_bar_k
    
    def bfs_close_lie_algebra(M_bar_k):
        n = len(M_bar_k)
        generators = list(range(n))
        queue = deque(generators)
        visited = set(generators)
        while queue:
            current = queue.popleft()
            for other in range(n):
                if other not in visited:
                    commutator = matrix_mul(matrix_sub(M_bar_k[current], identity_matrix(len(M_bar_k))), M_bar_k[other])
                    if frobenius_norm(commutator) < 1e-9:
                        visited.add(other)
                        queue.append(other)
        return len(visited)
    
    n_values = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    results = []
    
    for s in [4, 8, 16, 32, 64, 128]:
        for n in n_values:
            layers = build_bp(n)
            M_bar_k = extract_M_bar_k(layers)
            rho = bfs_close_lie_algebra(M_bar_k)
            results.append({
                "metric_name": "rho",
                "metric_value": rho,
                "instances_tested": 1,
                "conjecture_holds": rho <= 4 * math.log2(s) + 10,
                "counterexample": ""
            })
    
    canonical_layers = build_bp(12)
    canonical_M_bar_k = extract_M_bar_k(canonical_layers)
    rho_canonical = bfs_close_lie_algebra(canonical_M_bar_k)
    results.append({
        "metric_name": "rho",
        "metric_value": rho_canonical,
        "instances_tested": 1,
        "conjecture_holds": rho_canonical >= n_values[-1] // 2,
        "counterexample": ""
    })
    
    return {
        "seed": seed,
        "metrics": results
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    all_results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        all_results.extend(result["metrics"])
    
    rho_values = [r["metric_value"] for r in all_results if "rho" in r["metric_name"]]
    support_fraction = sum(1 for r in all_results if r["conjecture_holds"]) / len(all_results)
    
    if support_fraction >= 0.9:
        RESULT = f"SUPPORTED mean={sum(rho_values) / len(rho_values):.2f} std={math.sqrt(sum((x - sum(rho_values) / len(rho_values)) ** 2 for x in rho_values) / len(rho_values)):.2f} support_fraction={support_fraction:.2f}"
    elif any(not r["conjecture_holds"] for r in all_results):
        first_failing_seed = next(s for s, r in zip(seeds, all_results) if not r["conjecture_holds"])
        RESULT = f"FALSIFIED counterexample=\"{next(r['counterexample'] for r in all_results if not r['conjecture_holds'])}\" first_failing_seed={first_failing_seed}"
    else:
        RESULT = "INCONCLUSIVE insufficient evidence"
    
    print(RESULT)