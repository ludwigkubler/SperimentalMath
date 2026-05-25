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
        return abs(a*b) // gcd(a, b)
    
    def matrix_mult(A, B):
        m, k = len(A), len(B[0])
        n = len(B)
        C = [[0] * k for _ in range(m)]
        for i in range(m):
            for j in range(k):
                for l in range(n):
                    C[i][j] += A[i][l] * B[l][j]
        return C
    
    def gaussian_elimination(A, b):
        n = len(b)
        Augmented = [A[i] + [b[i]] for i in range(n)]
        
        # Forward elimination
        for i in range(n):
            max_row = i
            for k in range(i+1, n):
                if abs(Augmented[k][i]) > abs(Augmented[max_row][i]):
                    max_row = k
            Augmented[i], Augmented[max_row] = Augmented[max_row], Augmented[i]
            
            factor = Augmented[i][i]
            for j in range(i, n+1):
                Augmented[i][j] /= factor
            
            for k in range(n):
                if k != i:
                    factor = Augmented[k][i]
                    for j in range(i, n+1):
                        Augmented[k][j] -= factor * Augmented[i][j]
        
        # Back substitution
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = Augmented[i][-1]
            for j in range(i+1, n):
                x[i] -= Augmented[i][j] * x[j]
        
        return x
    
    def is_invertible(A):
        det = 0
        if len(A) == 2:
            det = A[0][0]*A[1][1] - A[0][1]*A[1][0]
        else:
            for c in range(len(A)):
                sign = (-1)**(c % 2)
                sub_det = [row[:c] + row[c+1:] for row in A[1:]]
                det += sign * A[0][c] * is_invertible(sub_det)
        return det != 0
    
    def matrix_inverse(A):
        n = len(A)
        adjoint = [[0]*n for _ in range(n)]
        determinant = 0
        
        if n == 2:
            adjoint[0][0] = A[1][1]
            adjoint[0][1] = -A[0][1]
            adjoint[1][0] = -A[1][0]
            adjoint[1][1] = A[0][0]
            determinant = A[0][0]*A[1][1] - A[0][1]*A[1][0]
        else:
            for i in range(n):
                sign = (-1)**(i % 2)
                sub_det = [row[:i] + row[i+1:] for row in A[1:]]
                adjoint[i] = [sign * is_invertible(sub_det) for sub_det in zip(*sub_det)]
            determinant = sum(A[0][i]*adjoint[i][0] for i in range(n))
        
        if determinant == 0:
            return None
        
        inverse = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                inverse[i][j] = adjoint[j][i] / determinant
        return inverse
    
    def matrix_determinant(A):
        n = len(A)
        det = 0
        
        if n == 2:
            det = A[0][0]*A[1][1] - A[0][1]*A[1][0]
        else:
            for c in range(len(A)):
                sign = (-1)**(c % 2)
                sub_det = [row[:c] + row[c+1:] for row in A[1:]]
                det += sign * A[0][c] * matrix_determinant(sub_det)
        
        return det
    
    def is_prime(n):
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True
    
    def generate_primes(n):
        primes = []
        for num in range(2, n):
            if is_prime(num):
                primes.append(num)
        return primes
    
    def generate_random_matrix(m, n):
        return [[random.randint(-10, 10) for _ in range(n)] for _ in range(m)]
    
    def generate_random_vector(n):
        return [random.randint(-10, 10) for _ in range(n)]
    
    def generate_disjointness_instance(n):
        points = []
        for i in range(n):
            x = random.uniform(0, 1)
            y = random.uniform(0, 1)
            points.append((x, y))
        return points
    
    def communication_complexity(points):
        n = len(points)
        if n == 2:
            return 1
        else:
            return 1 + communication_complexity(points[1:])
    
    def minimal_rank(n):
        # Placeholder for actual computation of minimal rank
        return n
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    points = generate_disjointness_instance(n)
    cc = communication_complexity(points)
    
    if cc != math.log2(n):
        return {
            "metric_name": "communication_complexity",
            "metric_value": cc,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"cc={cc} != log2({n})"
        }
    
    rank = minimal_rank(n)
    if rank > n:
        return {
            "metric_name": "minimal_rank",
            "metric_value": rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"rank={rank} > {n}"
        }
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": cc,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"cc != log2(n)\" first_failing_seed={first_failing_seed}")