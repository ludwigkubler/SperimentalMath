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

def matrix_multiply(A, B, m):
    n = len(B)
    p = len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    n = len(A)
    m = len(b)
    if n != m:
        raise ValueError("Incompatible dimensions")
    
    augmented_matrix = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j
        
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        
        factor = augmented_matrix[i][i]
        for j in range(i, m+1):
            augmented_matrix[i][j] /= factor
        
        for j in range(n):
            if j != i:
                factor = augmented_matrix[j][i]
                for k in range(m+1):
                    augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = augmented_matrix[i][-1]
        for j in range(i+1, n):
            x[i] -= augmented_matrix[i][j] * x[j]
    
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 20
    k = 3
    clause_density = 4
    
    # Generate a random 3-CNF formula with the given parameters
    num_clauses = int(n * (n - 1) * (n - 2) / 6 * clause_density / 3)
    clauses = []
    for _ in range(num_clauses):
        literals = [random.choice([i, -i]) for i in range(1, n+1)]
        random.shuffle(literals)
        clauses.append(literals[:3])
    
    # Compute the intersection lattice of k-element subsets
    from itertools import combinations
    subsets = list(combinations(range(1, n+1), k))
    lattice = []
    for subset in subsets:
        lattice.append([i in subset for i in range(1, n+1)])
    
    # Compute the polymatroid rank via the intersection lattice's rank function
    def rank(lattice):
        m = len(lattice)
        n = len(lattice[0])
        A = [[0] * n for _ in range(m)]
        b = [1] * m
        for i in range(m):
            for j in range(n):
                if lattice[i][j]:
                    A[i][j] = 1
        
        try:
            x = gaussian_elimination(A, b)
            return sum(x)
        except ValueError:
            return float('inf')
    
    rho_n_k = rank(lattice)
    
    # Measure DNF size via minimal clause cover
    def dnf_size(clauses):
        covered = [False] * len(clauses)
        while not all(covered):
            for i in range(len(clauses)):
                if not covered[i]:
                    if any(lit in clauses[i] for lit in set(range(1, n+1))):
                        covered[i] = True
        return sum(not c for c in covered)
    
    dnf_size_value = dnf_size(clauses)
    
    # Check if rho(n,k) <= log n implies DNF size >= n^1.5
    conjecture_holds = False
    counterexample = ""
    if rho_n_k <= math.log(n):
        if dnf_size_value < n**1.5:
            counterexample = f"rho({n},{k})={rho_n_k}, DNF size={dnf_size_value}"
    
    return {
        "metric_name": "DNF size",
        "metric_value": dnf_size_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3**j for i in range(5, 8) for j in range(5)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["counterexample"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["counterexample"])
        counterexample_desc = next(result["counterexample"] for result in results if result["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE insufficient data")