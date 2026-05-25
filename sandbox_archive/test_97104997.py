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
        while b != 0:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return abs(a*b) // gcd(a, b)
    
    def matrix_mul(A, B):
        rows_A, cols_A = len(A), len(A[0])
        rows_B, cols_B = len(B), len(B[0])
        result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
        for i in range(rows_A):
            for j in range(cols_B):
                for k in range(cols_A):
                    result[i][j] += A[i][k] * B[k][j]
        return result
    
    def matrix_det(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * matrix_det(submatrix)
        return det
    
    def gaussian_elimination(A, b):
        n = len(b)
        augmented_matrix = [A[i] + [b[i]] for i in range(n)]
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
        return [row[-1] for row in augmented_matrix]
    
    def is_prime(num):
        if num <= 1:
            return False
        if num <= 3:
            return True
        if num % 2 == 0 or num % 3 == 0:
            return False
        i = 5
        while i * i <= num:
            if num % i == 0 or num % (i + 2) == 0:
                return False
            i += 6
        return True
    
    def generate_primes(n):
        primes = []
        for possiblePrime in range(2, n + 1):
            isPrime = True
            for num in range(2, int(math.sqrt(possiblePrime)) + 1):
                if possiblePrime % num == 0:
                    isPrime = False
                    break
            if isPrime:
                primes.append(possiblePrime)
        return primes
    
    def generate_random_instance(n):
        points = [(random.uniform(-1, 1), random.uniform(-1, 1)) for _ in range(n)]
        disjoint = [random.choice([True, False]) for _ in range(n * (n - 1) // 2)]
        return points, disjoint
    
    def communication_complexity(points, disjoint):
        n = len(points)
        total_bits = 0
        for i in range(n):
            for j in range(i + 1, n):
                if disjoint[i * (n - 1) // 2 + j]:
                    total_bits += math.log2(n)
        return total_bits
    
    def minimal_rank(points):
        n = len(points)
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                if i == j:
                    A[i][j] = 1
                else:
                    A[i][j] = points[j][0] - points[i][0]
                    A[j][i] = points[j][1] - points[i][1]
        det = matrix_det(A)
        rank = sum(1 for row in A if any(row))
        return rank
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    points, disjoint = generate_random_instance(n)
    cc = communication_complexity(points, disjoint)
    mr = minimal_rank(points)
    
    if cc != math.log2(n):
        return {
            "metric_name": "communication_complexity",
            "metric_value": cc,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"cc={cc}, expected log2({n})=math.log2({n})"
        }
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mr,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes(30)
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = results[seeds.index(first_failing_seed)]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")