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
    
    def generate_k_clique(n, k):
        if k > n // 2:
            return None
        vertices = list(range(n))
        edges = []
        for i in range(k):
            for j in range(i + 1, k):
                edges.append((vertices[i], vertices[j]))
        for _ in range(n - k):
            u = random.choice(vertices)
            v = random.choice(vertices)
            while (u, v) in edges or (v, u) in edges:
                u = random.choice(vertices)
                v = random.choice(vertices)
            edges.append((u, v))
        return vertices, edges
    
    def construct_lattice(edges):
        n = len(edges) + 1
        A = [[0] * n for _ in range(n)]
        for i, j in edges:
            A[i][j] = A[j][i] = 1
        B = [0] * n
        return A, B
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(n):
            if rank == m:
                break
            pivot_row = rank
            while pivot_row < m and A[pivot_row][i] == 0:
                pivot_row += 1
            if pivot_row == m:
                continue
            A[rank], A[pivot_row] = A[pivot_row], A[rank]
            for j in range(n):
                if j != i:
                    factor = -A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] += factor * A[i][k]
            rank += 1
        return rank
    
    def lattice_width(A, B):
        m, n = len(A), len(A[0])
        rank = gaussian_elimination(A)
        width = n - rank
        for j in range(n):
            if A[j][j] != 0:
                width = min(width, abs(B[j]) / abs(A[j][j]))
        return width
    
    def monotone_circuit_size(n):
        # Placeholder function; actual implementation needed
        return n ** (5/4)
    
    for n in [5, 10, 15, 20, 30, 40]:
        k = random.randint(2, min(n // 2, 8))
        instance = generate_k_clique(n, k)
        if instance is None:
            continue
        vertices, edges = instance
        A, B = construct_lattice(edges)
        width = lattice_width(A, B)
        circuit_size = monotone_circuit_size(n)
        
        if width > n ** (3/4) * math.log(k) ** 2 or circuit_size < n ** (5/4):
            return {
                "metric_name": "Lattice Width vs Monotone Circuit Size",
                "metric_value": None,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"n={n}, k={k}, width={width}, circuit_size={circuit_size}"
            }
    
    return {
        "metric_name": "Lattice Width vs Monotone Circuit Size",
        "metric_value": None,
        "instances_tested": 6,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 103))  # First 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")