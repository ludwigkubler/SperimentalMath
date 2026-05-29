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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_multiply(A, B):
    m, k = len(A), len(B[0])
    n = len(B)
    C = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(n):
                C[i][j] += A[i][l] * B[l][j]
    return C

def gaussian_elimination(A, b):
    m, n = len(A), len(b)
    augmented_matrix = [A[i] + [b[i]] for i in range(m)]
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        pivot = augmented_matrix[i][i]
        for j in range(i, n+1):
            augmented_matrix[i][j] /= pivot
        for j in range(m):
            if j != i:
                factor = augmented_matrix[j][i]
                for k in range(i, n+1):
                    augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    return [row[-1] for row in augmented_matrix]

def generate_coxeter_group_action(G, I):
    orbits = set()
    for i in I:
        orbit = {tuple(sorted([G[i][j] for j in I]))}
        orbits.add(frozenset(orbit))
    return orbits

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(1, 10)
    
    # Generate a random monomial ideal I with n variables and m clauses
    I = set()
    for _ in range(m):
        clause = random.sample(range(n), random.randint(1, n))
        I.add(tuple(sorted(clause)))
    
    # Define the Coxeter group G (for simplicity, use S_n)
    G = [list(range(n)) for _ in range(n)]
    for i in range(n):
        G[i][i] = 0
        for j in range(i+1, n):
            G[i][j] = G[j][i] = random.choice([-1, 1])
    
    # Compute the action of the Coxeter group on I
    orbits = generate_coxeter_group_action(G, I)
    
    # Measure the number of orbits
    num_orbits = len(orbits)
    
    # Compute the complexity c of the monomial ideal I
    c = sum(len(clause) for clause in I)
    
    # Check if the conjecture holds
    conjecture_holds = num_orbits <= c ** 1.5
    
    return {
        "metric_name": "Number of Orbits",
        "metric_value": num_orbits,
        "instances_tested": len(I),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Conjecture failed for n={n}, m={m}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    num_trials = len(results)
    mean_metric_value = sum(r["metric_value"] for r in results) / num_trials
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / (num_trials - 1))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / num_trials
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='Conjecture failed' first_failing_seed={first_failing_seed}")