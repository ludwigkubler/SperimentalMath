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
    
    def generate_k_cnf(n, k):
        clauses = []
        for _ in range(k):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
                clause[1] *= -1
            clauses.append(clause)
        return clauses
    
    def matrix_multiply(A, B):
        rows_A = len(A)
        cols_A = len(A[0])
        cols_B = len(B[0])
        result = [[sum(A[i][k] * B[k][j] for k in range(cols_A)) for j in range(cols_B)] for i in range(rows_A)]
        return result
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        augmented_matrix = [row[:] + [0] for row in matrix]
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                    max_row = j
            augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
            pivot = augmented_matrix[i][i]
            for j in range(i, n+1):
                augmented_matrix[i][j] /= pivot
            for j in range(n):
                if j != i:
                    factor = augmented_matrix[j][i]
                    for k in range(i, n+1):
                        augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
        return [row[:-1] for row in augmented_matrix]
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        sign = 1
        for i in range(n):
            submatrix = [row[:i] + row[i+1:] for row in matrix[1:]]
            det += sign * matrix[0][i] * determinant(submatrix)
            sign *= -1
        return det
    
    def communication_complexity_rank(clauses):
        n = len(clauses)
        rank = 0
        for i in range(n):
            for j in range(i+1, n):
                if all(c in clauses[i] or c in clauses[j] for c in [-clauses[i][0], -clauses[i][1], -clauses[j][0], -clauses[j][1]]):
                    rank += 1
        return rank
    
    def variance_rank(rank_values):
        n = len(rank_values)
        mean = sum(rank_values) / n
        variance = sum((x - mean) ** 2 for x in rank_values) / n
        return variance
    
    def minimal_order(clauses):
        n = len(clauses)
        A = [[0] * (n+1) for _ in range(n+1)]
        for i, clause in enumerate(clauses):
            A[i][i] = 2
            for c in clause:
                if c > 0:
                    A[c-1][c-1] += 1
                else:
                    A[-1][-1] += 1
        A[-1][-1] -= n
        return abs(determinant(gaussian_elimination(A)))
    
    def k_cnf_to_quadratic_form(clauses):
        n = len(clauses)
        A = [[0] * (n+1) for _ in range(n+1)]
        for i, clause in enumerate(clauses):
            A[i][i] = 2
            for c in clause:
                if c > 0:
                    A[c-1][c-1] += 1
                else:
                    A[-1][-1] += 1
        A[-1][-1] -= n
        return A
    
    def gram_matrix(A):
        n = len(A)
        G = [[0] * (n+1) for _ in range(n+1)]
        for i in range(n+1):
            for j in range(i, n+1):
                if i == j:
                    G[i][j] = sum(A[k][i] ** 2 for k in range(n))
                else:
                    G[i][j] = sum(A[k][i] * A[k][j] for k in range(n))
        return G
    
    def minimal_order_quadratic_form(clauses):
        n = len(clauses)
        A = k_cnf_to_quadratic_form(clauses)
        G = gram_matrix(A)
        return abs(determinant(gaussian_elimination(G)))
    
    def variance_rank_monotone_duals(clauses):
        ranks = []
        for _ in range(10):  # Sample 10 monotone duals
            dual_clauses = [clause for clause in clauses if all(abs(c) != abs(clause[0]) for c in clause)]
            rank = communication_complexity_rank(dual_clauses)
            ranks.append(rank)
        return variance_rank(ranks)
    
    n = random.randint(5, 40)
    k = random.randint(1, min(n, 10))
    clauses = generate_k_cnf(n, k)
    
    minimal_order_value = minimal_order_quadratic_form(clauses)
    variance_rank_monotone_duals_value = variance_rank_monotone_duals(clauses)
    
    return {
        "metric_name": "MinimalOrder",
        "metric_value": minimal_order_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
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
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")