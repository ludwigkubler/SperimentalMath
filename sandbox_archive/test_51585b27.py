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

def generate_primes(count):
    primes = []
    num = 2
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def gaussian_elimination(A, b=None):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        if b is not None:
            b[i], b[max_row] = b[max_row], b[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
            if b is not None:
                b[j] -= factor * b[i]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x

def matrix_multiply(A, B):
    m = len(A)
    n = len(B[0])
    p = len(B)
    C = [[0.0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def sort_desc(lst):
    return sorted(lst, reverse=True)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([8, 10, 12, 14])
    degree = 3
    
    # Generate a 3-regular graph using the configuration model
    while True:
        A = [[0.0 for _ in range(n)] for _ in range(n)]
        degrees = [degree] * n
        edges = set()
        
        while any(d > 0 for d in degrees):
            u = random.randint(0, n - 1)
            if degrees[u] == 0:
                continue
            v = random.choice([i for i in range(n) if i != u and A[u][i] == 0])
            if degrees[v] > 0:
                edges.add((u, v))
                edges.add((v, u))
                degrees[u] -= 1
                degrees[v] -= 1
        
        # Check for multi-edges/self-loops
        if len(edges) != n * degree // 2:
            continue
        
        break
    
    # Convert to adjacency matrix
    A = [[0.0 for _ in range(n)] for _ in range(n)]
    for u, v in edges:
        A[u][v] = 1.0
        A[v][u] = 1.0
    
    # Compute eigenvalues of A^2
    A_squared = matrix_multiply(A, A)
    eigenvalues = gaussian_elimination(A_squared)
    
    # Compute SH(G)
    SH_G = sum(abs(3 - λ**2) for λ in eigenvalues)
    
    # Compute SOS2(G)
    lambda_min_A = min(eigenvalues)
    SOS2_G = (n / 4) * (3 - lambda_min_A)
    
    # Compute MaxCut(G)
    max_cut_value = 0
    for mask in range(1 << n):
        if bin(mask).count('1') != n // 2:
            continue
        cut_value = sum(A[i][j] for i in range(n) for j in range(i + 1, n) if (mask & (1 << i)) and (mask & (1 << j)))
        max_cut_value = max(max_cut_value, cut_value)
    
    # Compute the gap
    gap = SOS2_G - max_cut_value
    
    # Check the conjecture
    conjecture_holds = gap <= SH_G / 8
    counterexample = "" if conjecture_holds else f"SOS2(G) - MaxCut(G) > SH(G)/8"
    
    return {
        "metric_name": "SOS2_G - MaxCut(G)",
        "metric_value": gap,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        primes = generate_primes(30)
        seeds = primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_instances = sum(result["instances_tested"] for result in results)
    mean_value = sum(result["metric_value"] * result["instances_tested"] for result in results) / total_instances
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 * result["instances_tested"] for result in results) / total_instances)
    
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")