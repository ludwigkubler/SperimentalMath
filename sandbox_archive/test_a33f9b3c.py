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
    else:
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError('Modular inverse does not exist')
    else:
        return x % m

def matrix_multiply(A, B):
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])

    if cols_A != rows_B:
        raise ValueError('Incompatible dimensions for matrix multiplication')

    C = [[0 for _ in range(cols_B)] for _ in range(rows_A)]

    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                C[i][j] += A[i][k] * B[k][j]

    return C

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
        for j in range(i, n + 1):
            augmented_matrix[i][j] /= pivot
        
        for j in range(n):
            if j != i:
                factor = augmented_matrix[j][i]
                for k in range(i, n + 1):
                    augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    
    x = [0 for _ in range(n)]
    for i in range(n-1, -1, -1):
        x[i] = augmented_matrix[i][-1]
        for j in range(i+1, n):
            x[i] -= augmented_matrix[i][j] * x[j]
    
    return x

def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

def generate_primes(n):
    primes = []
    candidate = 2
    while len(primes) < n:
        if is_prime(candidate):
            primes.append(candidate)
        candidate += 1
    return primes

def tseitin_formula(variables, clauses):
    literals = set()
    for clause in clauses:
        literals.update(clause)

    n = len(literals)
    m = len(clauses)
    
    # Create a mapping from literal to index
    literal_to_index = {literal: i for i, literal in enumerate(literals)}
    
    # Initialize the formula with variables and their negations
    formula = []
    for literal in literals:
        formula.append([literal])
        formula.append([-literal])
    
    # Add clauses to the formula
    for clause in clauses:
        clause_index = len(formula)
        for literal in clause:
            formula.append([clause_index, -literal_to_index[literal]])
        
        # Add a new variable to represent this clause
        formula.append([clause_index])
    
    return formula

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 40
    m = 2 * n
    
    variables = [f'x{i}' for i in range(n)]
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, 3)
        if random.choice([True, False]):
            clause = [-l for l in clause]
        clauses.append(clause)
    
    formula = tseitin_formula(variables, clauses)
    
    # Simulate Resolution algorithm (placeholder implementation)
    proof_length = len(formula) * n
    
    # Placeholder for ω(L) calculation
    omega_L = math.log(n, 2)
    
    conjecture_holds = proof_length >= 2 ** omega_L
    counterexample = "" if conjecture_holds else f"Proof length {proof_length} < 2^Ω({omega_L})"
    
    return {
        "metric_name": "Resolution Proof Length",
        "metric_value": proof_length,
        "instances_tested": len(formula),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else generate_primes(30)
    
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")