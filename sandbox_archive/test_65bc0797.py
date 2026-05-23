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
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return abs(a * b) // gcd(a, b)
    
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    
    def mod_inverse(a, m):
        gcd, x, _ = extended_gcd(a, m)
        if gcd != 1:
            raise ValueError("Modular inverse does not exist")
        else:
            return x % m
    
    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def matrix_power(M, k):
        n = len(M)
        result = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
        while k > 0:
            if k % 2 == 1:
                result = matrix_multiply(result, M)
            M = matrix_multiply(M, M)
            k //= 2
        return result
    
    def is_invertible(matrix):
        n = len(matrix)
        det = 0
        for i in range(n):
            minor = [row[:i] + row[i+1:] for row in matrix[1:]]
            sign = (-1) ** (i % 2)
            sub_det = determinant(minor)
            det += sign * matrix[0][i] * sub_det
        return det != 0
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        elif n == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        else:
            det = 0
            for i in range(n):
                minor = [row[:i] + row[i+1:] for row in matrix[1:]]
                sign = (-1) ** (i % 2)
                sub_det = determinant(minor)
                det += sign * matrix[0][i] * sub_det
            return det
    
    def rank(matrix):
        n, m = len(matrix), len(matrix[0])
        augmented_matrix = [row + [0] for row in matrix]
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                    max_row = j
            augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
            pivot = augmented_matrix[i][i]
            for j in range(i, m+1):
                augmented_matrix[i][j] /= pivot
            for j in range(n):
                if j != i:
                    factor = augmented_matrix[j][i]
                    for k in range(m+1):
                        augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
        rank = sum(1 for row in augmented_matrix if any(row))
        return rank
    
    def boolean_circuit_weight(n, D):
        # Placeholder function to simulate circuit weight calculation
        # This is a dummy implementation and should be replaced with actual logic
        return 2 ** (n - D)
    
    n = random.randint(5, 40)
    D = random.randint(1, n)
    f = [random.randint(0, 1) for _ in range(2**n)]
    
    rho_f = rank(f)
    weight = boolean_circuit_weight(n, D)
    
    metric_value = abs(rho_f - math.log2(weight))
    conjecture_holds = metric_value <= 3
    counterexample = "" if conjecture_holds else f"rho(f)={rho_f}, weight={weight}"
    
    return {
        "metric_name": "Rank vs Circuit Weight",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30)) + [101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']:.6f}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean = sum(r["metric_value"] for r in results) / len(results)
        std = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean:.6f} std={std:.6f} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")