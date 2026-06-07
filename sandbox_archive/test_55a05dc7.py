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

# Helper functions for linear algebra and group operations
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
    augmented_matrix = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        
        # Eliminate below pivot
        for j in range(i+1, n):
            factor = augmented_matrix[j][i] / augmented_matrix[i][i]
            for k in range(n + 1):
                augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    
    # Back substitution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = augmented_matrix[i][-1]
        for j in range(i+1, n):
            x[i] -= augmented_matrix[i][j] * x[j]
        x[i] /= augmented_matrix[i][i]
    
    return x

def matrix_inverse(A):
    n = len(A)
    I = [[Fraction(0) if i != j else Fraction(1) for j in range(n)] for i in range(n)]
    A_augmented = [A[i] + I[i] for i in range(n)]
    
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A_augmented[j][i]) > abs(A_augmented[max_row][i]):
                max_row = j
        A_augmented[i], A_augmented[max_row] = A_augmented[max_row], A_augmented[i]
        
        # Eliminate below pivot
        for j in range(i+1, n):
            factor = A_augmented[j][i] / A_augmented[i][i]
            for k in range(2 * n):
                A_augmented[j][k] -= factor * A_augmented[i][k]
    
    # Back substitution
    for i in range(n):
        x_i = Fraction(A_augmented[i][-1])
        for j in range(i+1, n):
            x_i -= A_augmented[i][j] * Fraction(A_augmented[j][-1])
        x_i /= A_augmented[i][i]
        
        # Normalize row
        for k in range(2 * n):
            A_augmented[i][k] *= x_i
    
    return [row[n:] for row in A_augmented]

# Function to generate a random CNF with n variables and m clauses
def generate_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = set()
        while len(clause) < 3:
            var = random.randint(1, n)
            sign = random.choice([True, False])
            if (var, not sign) not in clause and (-var, sign) not in clause:
                clause.add((var, sign))
        cnf.append(clause)
    return cnf

# Function to compute the incidence algebra of a CNF
def incidence_algebra(cnf):
    n = max(abs(var) for var, _ in cnf)
    algebra = [[0] * (n + 1) for _ in range(n + 1)]
    
    for clause in cnf:
        for i in range(1, n + 1):
            if (i, True) not in clause and (-i, False) not in clause:
                for j in range(i + 1, n + 1):
                    if (j, True) not in clause and (-j, False) not in clause:
                        algebra[i][j] += 1
    return algebra

# Function to compute the minimal depth of a Deligne-Lusztig tree
def deligne_lusztig_tree_depth(algebra):
    n = len(algebra)
    adjacency_matrix = [[0] * (n + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            if algebra[i][j] > 0:
                adjacency_matrix[i][j] = 1
                adjacency_matrix[j][i] = 1
    
    # Find the maximum independent set
    max_independent_set = []
    visited = [False] * (n + 1)
    
    def dfs(node):
        if visited[node]:
            return False
        visited[node] = True
        max_independent_set.append(node)
        for neighbor in range(1, n + 1):
            if adjacency_matrix[node][neighbor] == 1:
                if not dfs(neighbor):
                    return False
        return True
    
    for node in range(1, n + 1):
        if not visited[node]:
            dfs(node)
    
    # The depth is the size of the maximum independent set minus one
    return len(max_independent_set) - 1

# Function to compute the communication complexity rank variance
def communication_complexity_rank_variance(cnf):
    n = max(abs(var) for var, _ in cnf)
    incidence_matrix = [[0] * (n + 1) for _ in range(n + 1)]
    
    for clause in cnf:
        for i in range(1, n + 1):
            if (i, True) not in clause and (-i, False) not in clause:
                for j in range(i + 1, n + 1):
                    if (j, True) not in clause and (-j, False) not in clause:
                        incidence_matrix[i][j] += 1
    
    # Compute the rank of the incidence matrix
    rank = len(gaussian_elimination(incidence_matrix, [0] * (n + 1)))
    
    # The variance is the difference between the maximum and minimum ranks
    return n - rank

# Function to run a single trial for a given seed
def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        m = random.randint(n, n * (n - 1))
        cnf = generate_cnf(n, m)
        
        algebra = incidence_algebra(cnf)
        depth = deligne_lusztig_tree_depth(algebra)
        variance = communication_complexity_rank_variance(cnf)
        
        results.append((depth, variance))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }
    
    mean_depth = sum(depth for depth, _ in results) / len(results)
    mean_variance = sum(variance for _, variance in results) / len(results)
    correlation_coefficient = sum((depth - mean_depth) * (variance - mean_variance) for depth, variance in results) / (len(results) * math.sqrt(sum((depth - mean_depth) ** 2 for depth, _ in results)) * math.sqrt(sum((variance - mean_variance) ** 2 for _, variance in results)))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for n, _ in results),
        "conjecture_holds": correlation_coefficient > 0.95,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(2, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"low_correlation\" first_failing_seed={first_failing_seed}")