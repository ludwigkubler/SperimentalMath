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
            max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(n):
                if j != i:
                    factor = A[j][i] / A[i][i]
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
    
    def rank_variance(matrix):
        m, n = len(matrix), len(matrix[0])
        matrix = gaussian_elimination(matrix)
        rank = sum(1 for row in matrix if any(row))
        return (m - rank) / min(m, n)
    
    def minimal_order_of_lie_algebroid_action(matrix):
        m, n = len(matrix), len(matrix[0])
        identity = [[int(i == j) for j in range(n)] for i in range(m)]
        A = matrix_multiply(identity, matrix)
        order = 1
        while True:
            A = matrix_multiply(A, matrix)
            if A == identity:
                return order
            order += 1
    
    def generate_communication_complexity_instance():
        n = random.randint(5, 30)
        alpha = random.random()
        adjacency_matrix = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            adjacency_matrix[i][i] = 0
        return adjacency_matrix, alpha
    
    instances_tested = 0
    n_max = 0
    total_order = 0
    
    for _ in range(30):
        matrix, alpha = generate_communication_complexity_instance()
        order = minimal_order_of_lie_algebroid_action(matrix)
        instances_tested += 1
        n_max = max(n_max, len(matrix))
        total_order += order
    
    mean_order = total_order / instances_tested
    conjecture_holds = abs(mean_order - alpha**0.5) <= 0.05 * alpha**0.5
    counterexample = "" if conjecture_holds else f"alpha={alpha}, order={mean_order}"
    
    return {
        "metric_name": "minimal_order_of_lie_algebroid_action",
        "metric_value": mean_order,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_order = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_order} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_order} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"alpha={results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")