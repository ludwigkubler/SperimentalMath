# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def gaussian_elimination(A, b):
        n = len(A)
        augmented_matrix = [row + [b[i]] for i, row in enumerate(A)]
        for i in range(n):
            max_row = max(range(i, n), key=lambda r: abs(augmented_matrix[r][i]))
            augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
            pivot = augmented_matrix[i][i]
            if pivot == 0:
                continue
            for j in range(n + 1):
                augmented_matrix[i][j] /= pivot
            for k in range(n):
                if k != i and abs(augmented_matrix[k][i]) > 0:
                    factor = augmented_matrix[k][i]
                    for j in range(n + 1):
                        augmented_matrix[k][j] -= factor * augmented_matrix[i][j]
        return [row[-1] for row in augmented_matrix]
    
    def communication_complexity(A, rank):
        n = len(A)
        if rank == 0:
            return 0
        B = [[A[i][j] for j in range(rank)] for i in range(n)]
        c = gaussian_elimination(B, [1] * rank)
        return sum(abs(x) for x in c)
    
    def minimal_automorphic_rank(A):
        n = len(A)
        ranks = set()
        for r in range(1, n + 1):
            B = [[A[i][j] for j in range(r)] for i in range(n)]
            if gaussian_elimination(B, [1] * r) == [0] * r:
                ranks.add(r)
        return min(ranks)
    
    def correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = (sum((x[i] - mean_x) ** 2 for i in range(n)) / n) ** 0.5
        std_y = (sum((y[i] - mean_y) ** 2 for i in range(n)) / n) ** 0.5
        return cov_xy / (std_x * std_y)
    
    def generate_random_arrangement(n):
        A = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        return A
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    complexities = []
    
    for n in n_values:
        for _ in range(5):
            A = generate_random_arrangement(n)
            rank = minimal_automorphic_rank(A)
            complexity = communication_complexity(A, rank)
            ranks.append(rank)
            complexities.append(complexity)
    
    if not ranks or not complexities:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation = correlation_coefficient(ranks, complexities)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation,
        "instances_tested": len(ranks),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation) >= 0.95,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results)) ** 0.5
    support_fraction = sum(r["conjecture_holds"] for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=not_enough_data")