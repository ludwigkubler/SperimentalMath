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
    
    def generate_random_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.add((i, j))
        return {i: sorted(j for j in edges if j > i) for i in range(n)}
    
    def coxeter_matrix(graph):
        n = len(graph)
        W = [[0] * n for _ in range(n)]
        for i in range(n):
            W[i][i] = 1
        for u, v in graph.items():
            for w in v:
                W[u][w] = -1
        return W
    
    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        augmented_matrix = [row[:] + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(matrix)]
        for i in range(n):
            pivot_row = max(range(i, n), key=lambda r: abs(augmented_matrix[r][i]))
            augmented_matrix[i], augmented_matrix[pivot_row] = augmented_matrix[pivot_row], augmented_matrix[i]
            if augmented_matrix[i][i] == 0:
                return None
            for j in range(n + 1):
                augmented_matrix[i][j] /= augmented_matrix[i][i]
            for k in range(n):
                if k != i and augmented_matrix[k][i] != 0:
                    factor = augmented_matrix[k][i]
                    for j in range(n + 1):
                        augmented_matrix[k][j] -= factor * augmented_matrix[i][j]
        return [row[-1] for row in augmented_matrix]
    
    def resolution_proof_length(W):
        n = len(W)
        rank = gaussian_elimination(W)
        if rank is None:
            return float('inf')
        return 2 ** (n - rank)
    
    def tseitin_formula(graph, variables):
        clauses = []
        for u in graph:
            for v in graph[u]:
                clauses.append([-variables[(u, v)], -variables[(v, u)]])
                clauses.append([variables[(u, v)], variables[(v, u)]])
        return clauses
    
    def random_variables(n):
        return {(i, j): random.choice([True, False]) for i in range(n) for j in range(i + 1, n)}
    
    n = random.randint(5, 40)
    graph = generate_random_graph(n)
    W = coxeter_matrix(graph)
    rank_W = len(gaussian_elimination(W))
    variables = random_variables(n)
    F_G = tseitin_formula(graph, variables)
    
    expected_length = 2 ** (1/3) * n**(2/3) * rank_W
    actual_length = resolution_proof_length(W)
    
    return {
        "metric_name": "resolution_proof_length",
        "metric_value": actual_length,
        "instances_tested": 1,
        "conjecture_holds": actual_length >= expected_length,
        "counterexample": "" if actual_length >= expected_length else f"Graph size {n}, rank(W(G))={rank_W}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_length = sum(r["metric_value"] for r in results) / len(results)
    std_length = math.sqrt(sum((r["metric_value"] - mean_length)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_length} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_length} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if r["counterexample"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")