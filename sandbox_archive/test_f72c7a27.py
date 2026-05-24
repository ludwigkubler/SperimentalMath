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
    
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    def generate_primes(k):
        primes = []
        num = 2
        while len(primes) < k:
            if is_prime(num):
                primes.append(num)
            num += 1
        return primes
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return abs(a * b) // gcd(a, b)
    
    def matrix_mult(A, B):
        rows_A, cols_A = len(A), len(A[0])
        rows_B, cols_B = len(B), len(B[0])
        if cols_A != rows_B:
            raise ValueError("Incompatible dimensions for matrix multiplication")
        result = [[sum(A[i][k] * B[k][j] for k in range(cols_A)) for j in range(cols_B)] for i in range(rows_A)]
        return result
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        augmented_matrix = [row[:] + [0] for row in matrix]
        rank = 0
        for col in range(n):
            if rank == n:
                break
            pivot_row = -1
            for i in range(rank, n):
                if abs(augmented_matrix[i][col]) > 1e-9:
                    pivot_row = i
                    break
            if pivot_row == -1:
                continue
            augmented_matrix[pivot_row], augmented_matrix[rank] = augmented_matrix[rank], augmented_matrix[pivot_row]
            for i in range(n):
                if i != rank and abs(augmented_matrix[i][col]) > 1e-9:
                    factor = augmented_matrix[i][col] / augmented_matrix[rank][col]
                    for j in range(n + 1):
                        augmented_matrix[i][j] -= factor * augmented_matrix[rank][j]
            rank += 1
        return rank
    
    def disjointness_function(x, y):
        return int(all(xi != yi for xi, yi in zip(x, y)))
    
    def kostant_partition_function(n):
        if n > 4:
            return "mapping_undefined"
        # Placeholder implementation for Kostant partition function
        # This is a dummy function and should be replaced with actual computation
        return n
    
    def communication_complexity(f):
        # Placeholder implementation for communication complexity
        # This is a dummy function and should be replaced with actual computation
        return n
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    x = [random.randint(0, 1) for _ in range(n)]
    y = [random.randint(0, 1) for _ in range(n)]
    
    f_value = disjointness_function(x, y)
    rank = kostant_partition_function(n)
    comm_complexity = communication_complexity(f_value)
    
    metric_name = "minimal_rank"
    metric_value = rank
    instances_tested = 1
    conjecture_holds = rank >= n ** (1/3)
    counterexample = "" if conjecture_holds else f"n={n}, rank={rank}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[first_failing_seed]['instances_tested']}, rank={results[first_failing_seed]['metric_value']}\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE no seeds tested")