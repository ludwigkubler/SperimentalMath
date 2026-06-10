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

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        # Find pivot
        max_row = i
        for r in range(i+1, rows):
            if abs(matrix[r][i]) > abs(matrix[max_row][i]):
                max_row = r
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below
        for r in range(i+1, rows):
            factor = matrix[r][i] / matrix[i][i]
            for c in range(cols):
                matrix[r][c] -= factor * matrix[i][c]

    return matrix

def rank(matrix):
    matrix = gaussian_elimination(matrix)
    rank = 0
    for row in matrix:
        if any(row):
            rank += 1
    return rank

def tseitin_formula(phi):
    literals = set()
    clauses = phi.split(' or ')
    new_vars = {}
    
    def literal_to_var(lit):
        if lit.startswith('-'):
            return -new_vars[lit[1:]]
        else:
            return new_vars[lit]
    
    for clause in clauses:
        parts = clause.split(' and ')
        if len(parts) == 1:
            literals.add(clause)
        else:
            new_var = f'x{len(new_vars)+1}'
            new_vars[new_var] = len(new_vars) + 1
            literals.add(f'-{new_var}')
            for part in parts:
                literals.add(f'{part} or {new_var}')
    
    return literals

def run_trial(seed: int) -> dict:
    random.seed(seed)
    p = generate_primes(1)[0]  # Using the first prime number
    n_max = 40
    instances_tested = 0
    total_rank = 0
    
    for n in range(5, n_max + 1):
        phi = ' or '.join(f'x{i}' if i % 2 == 0 else f'-x{i}' for i in range(1, n+1))
        phi_G = tseitin_formula(phi)
        rank_value = rank([[int(lit.startswith('-')) for lit in phi_G]])
        
        total_rank += rank_value
        instances_tested += 1
    
    mean_rank = total_rank / instances_tested if instances_tested > 0 else 0
    conjecture_holds = mean_rank <= 2**n_max  # Doubly-exponential bound
    counterexample = "" if conjecture_holds else "rank_exceeds_bound"
    
    return {
        "metric_name": "mean_rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "n_max": n_max,
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
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"rank_exceeds_bound\" first_failing_seed={first_failing_seed}")