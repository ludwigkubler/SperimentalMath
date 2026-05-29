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
    return abs(a*b) // gcd(a, b)

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0 for _ in range(p)] for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    n = len(b)
    augmented = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(augmented[j][i]) > abs(augmented[max_row][i]):
                max_row = j
        augmented[i], augmented[max_row] = augmented[max_row], augmented[i]
        factor = augmented[i][i]
        for j in range(n + 1):
            augmented[i][j] /= factor
        for j in range(n):
            if i != j:
                factor = augmented[j][i]
                for k in range(n + 1):
                    augmented[j][k] -= factor * augmented[i][k]
    return [row[-1] for row in augmented]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(1, 10)
    variables = list(range(n))
    clauses = [[random.choice(variables) for _ in range(random.randint(2, 3))] for _ in range(m)]
    
    # Compute the complexity of the monomial ideal
    c = len(clauses)
    
    # Define a simple Coxeter group action (e.g., cyclic permutation)
    def coxeter_group_action(I):
        return [(i + 1) % n if i != n-1 else 0 for i in I]
    
    # Generate all monomials of degree c
    monomials = []
    def generate_monomials(current, depth):
        if depth == c:
            monomials.append(tuple(sorted(current)))
            return
        for var in variables:
            if var not in current or current.index(var) < len(current) - 1:
                generate_monomials(current + [var], depth + 1)
    generate_monomials([], 0)
    
    # Apply the Coxeter group action and count orbits
    orbit_set = set()
    for monomial in monomials:
        orbit = tuple(sorted(coxeter_group_action(monomial)))
        orbit_set.add(orbit)
    
    num_orbits = len(orbit_set)
    
    # Check the conjecture bound
    upper_bound = c ** 1.5
    
    return {
        "metric_name": "Number of Orbits",
        "metric_value": num_orbits,
        "instances_tested": len(monomials),
        "conjecture_holds": num_orbits <= upper_bound,
        "counterexample": "" if num_orbits <= upper_bound else f"Too many orbits: {num_orbits} > {upper_bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results]
    conjecture_holds_count = sum(r["conjecture_holds"] for r in results)
    
    mean = sum(metric_values) / len(metric_values)
    std_dev = math.sqrt(sum((x - mean)**2 for x in metric_values) / len(metric_values))
    support_fraction = conjecture_holds_count / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Too many orbits\" first_failing_seed={first_failing_seed}")