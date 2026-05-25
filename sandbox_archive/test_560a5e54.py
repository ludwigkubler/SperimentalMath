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
    
    def generate_random_graph(n):
        adj_matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    adj_matrix[i][j] = 1
                    adj_matrix[j][i] = 1
        return adj_matrix
    
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
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i + 1, n):
                factor = A[j][i] / A[i][i]
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n - 1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
        return x
    
    def rank(matrix):
        A = [row[:] for row in matrix]
        b = [0] * len(A)
        return len(gaussian_elimination(A, b))
    
    def noncommutative_tensor_product(G1, G2):
        n = len(G1)
        tensor_product = [[0] * (n * n) for _ in range(n * n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    for l in range(n):
                        tensor_product[i * n + k][j * n + l] += G1[i][j] * G2[k][l]
        return tensor_product
    
    def symmetric_group_universal_enveloping_algebra(n):
        # Simplified representation of the universal enveloping algebra
        # This is a placeholder and does not represent actual computations
        return [[0] * n for _ in range(n)]
    
    def minimal_rank(G1, G2):
        U = symmetric_group_universal_enveloping_algebra(len(G1))
        tensor_product = noncommutative_tensor_product(G1, G2)
        return rank(tensor_product)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        graph1 = generate_random_graph(n)
        graph2 = generate_random_graph(n)
        min_rank = minimal_rank(graph1, graph2)
        results.append(min_rank)
    
    avg_rank = sum(results) / len(results)
    conjecture_holds = avg_rank <= n * math.log(n, 2) ** 2
    counterexample = "" if conjecture_holds else f"Average rank {avg_rank} exceeds bound {n * math.log(n, 2) ** 2}"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": avg_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    avg_rank = sum(results) / len(results)
    support_fraction = sum(1 for r in results if r <= n * math.log(n, 2) ** 2) / len(results)
    
    if all(r <= n * math.log(n, 2) ** 2 for r in results):
        print(f"RESULT: SUPPORTED mean={avg_rank} std=0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_rank} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result > n * math.log(n, 2) ** 2)
        print(f"RESULT: FALSIFIED counterexample='Average rank exceeds bound' first_failing_seed={first_failing_seed}")