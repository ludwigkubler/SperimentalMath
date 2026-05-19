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
    
    def reverse_bfs(g, start):
        n = len(g)
        visited = [False] * n
        queue = [start]
        visited[start] = True
        cone = set()
        while queue:
            u = queue.pop(0)
            cone.add(u)
            for v in range(n):
                if g[u][v] and not visited[v]:
                    visited[v] = True
                    queue.append(v)
        return cone
    
    def matrix_mult(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def power_method(M, max_iter=30):
        n = len(M)
        v = [1.0 / math.sqrt(n)] * n
        for _ in range(max_iter):
            w = matrix_mult(M, v)
            w_norm = sum(x ** 2 for x in w) ** 0.5
            v = [x / w_norm for x in w]
        return max(w), v
    
    def trace(matrix):
        return sum(matrix[i][i] for i in range(len(matrix)))
    
    def lambda_max(matrix):
        _, eigenvalues = power_method(matrix)
        return max(eigenvalues)
    
    def psi(C, d):
        K = [[0] * len(C) for _ in range(len(C))]
        for g in C:
            cone_g = reverse_bfs(g, 0)
            for h in C:
                cone_h = reverse_bfs(h, 0)
                intersection_size = sum(1 for x in cone_g if x in cone_h)
                K[C.index(g)][C.index(h)] = intersection_size / len(C)
        trace_K = trace(K)
        lambda_max_K = lambda_max(K)
        return trace_K / lambda_max_K
    
    def compute_r(C, d):
        return psi(C, d) ** (1 / (d - 1)) / math.log2(len(C))
    
    def generate_ac0_circuit(n, depth):
        if depth == 2:
            circuit = [random.sample(range(1, n), n // 2) for _ in range(n)]
            circuit.append(random.choices([1, -1], k=n))
        elif depth == 3:
            block_size = int(math.ceil(math.sqrt(n)))
            blocks = [generate_ac0_circuit(block_size, 2) for _ in range(n // block_size + 1)]
            circuit = []
            for i in range(n):
                if i % block_size < block_size - 1:
                    circuit.append(blocks[i // block_size][i % block_size])
                else:
                    circuit.append([sum(x for x in blocks[j][i % block_size] for j in range(i // block_size + 1)) % 2])
        return circuit
    
    def add_redundancy(g):
        n = len(g)
        for _ in range(n):
            g[random.randint(0, n - 1)][random.randint(0, n - 1)] = 1
        return g
    
    def generate_instance(n, d):
        circuit = generate_ac0_circuit(n, d)
        for _ in range(30):
            circuit = add_redundancy(circuit)
        return circuit
    
    n_values = [4, 6, 8, 10, 12, 14, 16, 20, 24]
    d_values = [2, 3]
    results = []
    
    for n in n_values:
        for d in d_values:
            instances_tested = 0
            max_r = -math.inf
            for _ in range(30):
                instance = generate_instance(n, d)
                r = compute_r(instance, d)
                instances_tested += 1
                if r > max_r:
                    max_r = r
            results.append({
                "n": n,
                "d": d,
                "instances_tested": instances_tested,
                "max_r": max_r
            })
    
    metric_value = sum(result["max_r"] for result in results) / len(results)
    conjecture_holds = all(result["max_r"] <= 8 for result in results)
    counterexample = "" if conjecture_holds else f"max r > 8 at n={results[0]['n']}, d={results[0]['d']}"
    
    return {
        "metric_name": "max_r",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["max_r"] <= 8 for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(result["max_r"] > 8 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["max_r"] > 8)
        print(f"RESULT: FALSIFIED counterexample=\"max r > 8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unsupported_operation")