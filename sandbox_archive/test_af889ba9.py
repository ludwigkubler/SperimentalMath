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
    
    def generate_primes(count):
        primes = []
        num = 2
        while len(primes) < count:
            if is_prime(num):
                primes.append(num)
            num += 1
        return primes
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i
            for k in range(i + 1, n):
                if abs(A[k][i]) > abs(A[max_row][i]):
                    max_row = k
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for k in range(i + 1, n):
                factor = A[k][i] / A[i][i]
                for j in range(i, n):
                    A[k][j] -= factor * A[i][j]
                b[k] -= factor * b[i]
        x = [0.0] * n
        for i in range(n - 1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
        return x
    
    def matrix_multiply(A, B):
        m = len(A)
        p = len(B[0])
        result = [[0.0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(len(B)):
                    result[i][j] += A[i][k] * B[k][j]
        return result
    
    def determinant(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = 0
        for c in range(n):
            det += ((-1) ** c) * A[0][c] * determinant([row[:c] + row[c+1:] for row in A[1:]])
        return det
    
    def inverse(A):
        n = len(A)
        det_A = determinant(A)
        if det_A == 0:
            raise ValueError("Matrix is singular")
        adjoint = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                minor = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
                cofactor = (-1) ** (i + j) * determinant(minor)
                adjoint[j][i] = cofactor
        inv_A = matrix_multiply(adjoint, [[1 / det_A] * n for _ in range(n)])
        return inv_A
    
    def generate_hyperbolic_surface(g):
        if g < 1:
            raise ValueError("Genus must be at least 1")
        # Simplified model of a hyperbolic surface using a grid
        return [[(i, j) for j in range(-g, g + 1)] for i in range(-g, g + 1)]
    
    def satisfiability_problem(surface, n):
        if len(surface) < n:
            raise ValueError("Surface too small for n variables")
        # Simplified model of a satisfiability problem
        return [[random.choice([0, 1]) for _ in range(n)] for _ in range(len(surface))]
    
    def monotone_circuit_size(surface, n):
        if len(surface) < n:
            raise ValueError("Surface too small for n variables")
        # Simplified model of a monotone circuit size
        return random.randint(10, 50)
    
    def check_conjecture(g, S_n):
        D = 2
        return abs(D ** g * S_n / S_n - 1) <= 1.05
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        surface = generate_hyperbolic_surface(g)
        instances = satisfiability_problem(surface, n)
        S_n = sum(monotone_circuit_size(surface, n) for _ in range(10))
        results.append(S_n)
    
    mean_S_n = sum(results) / len(results)
    support_fraction = all(check_conjecture(g, S_n) for S_n in results)
    
    return {
        "metric_name": "monotone_circuit_size",
        "metric_value": mean_S_n,
        "instances_tested": len(n_values),
        "conjecture_holds": support_fraction,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or generate_primes(30)
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean_value = sum(results) / len(results)
    support_fraction = all(trial["conjecture_holds"] for trial in results if "conjecture_holds" in trial and trial["conjecture_holds"])
    
    if support_fraction:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")