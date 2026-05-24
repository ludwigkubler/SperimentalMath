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
        if n < k:
            return None
        vertices = list(range(n))
        edges = []
        for i in range(k):
            for j in range(i + 1, k):
                edges.append((vertices[i], vertices[j]))
        return vertices, edges
    
    def matrix_multiplication(A, B):
        rows_A, cols_A = len(A), len(A[0])
        rows_B, cols_B = len(B), len(B[0])
        if cols_A != rows_B:
            raise ValueError("Incompatible dimensions for matrix multiplication")
        result = [[sum(A[i][k] * B[k][j] for k in range(cols_A)) for j in range(cols_B)] for i in range(rows_A)]
        return result
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        augmented_matrix = [row + [1 if i == j else 0 for j in range(cols)] for i, row in enumerate(matrix)]
        for i in range(rows):
            max_row = max(range(i, rows), key=lambda r: abs(augmented_matrix[r][i]))
            augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
            pivot = augmented_matrix[i][i]
            if pivot == 0:
                continue
            for j in range(cols + 1):
                augmented_matrix[i][j] /= pivot
            for k in range(rows):
                if k != i and augmented_matrix[k][i] != 0:
                    factor = augmented_matrix[k][i]
                    for j in range(cols + 1):
                        augmented_matrix[k][j] -= factor * augmented_matrix[i][j]
        rank = sum(1 for row in augmented_matrix if any(row[j] != 0 for j in range(cols)))
        return rank
    
    def compute_geometric_entanglement_rank(n, k):
        vertices, edges = generate_k_clique(n, k)
        if vertices is None:
            return None
        adjacency_matrix = [[1 if (i, j) in edges or (j, i) in edges else 0 for j in range(n)] for i in range(n)]
        rank = gaussian_elimination(adjacency_matrix)
        return rank
    
    def compute_sum_of_squares_circuit_size(n):
        # Placeholder function to simulate sum-of-squares circuit size
        return random.randint(1, n * (n - 1) // 2)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            rank = compute_geometric_entanglement_rank(n, random.randint(2, n - 1))
            if rank is None:
                continue
            circuit_size = compute_sum_of_squares_circuit_size(n)
            results.append({
                "metric_name": "Rank vs Circuit Size",
                "metric_value": rank / n,
                "instances_tested": 1,
                "conjecture_holds": rank >= n * 0.8 and circuit_size <= 3,
                "counterexample": ""
            })
    
    if not results:
        return {
            "metric_name": "Rank vs Circuit Size",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }
    
    mean_metric = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "metric_name": "Rank vs Circuit Size",
        "metric_value": mean_metric,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.95,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("seed" in r for r in results):
        mean_metric = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.95:
            print(f"RESULT: SUPPORTED mean={mean_metric} std={math.sqrt(sum((r['metric_value'] - mean_metric) ** 2 for r in results) / len(results))} support_fraction={support_fraction}")
        else:
            first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
            print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE missing_seed_data")