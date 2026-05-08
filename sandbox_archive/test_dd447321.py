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
        raise ValueError("Inverse doesn't exist")
    else:
        return x % m

def matrix_multiply(A, B, p):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % p
    return C

def gaussian_elimination(A, b, p):
    n = len(A)
    augmented_matrix = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        pivot = augmented_matrix[i][i]
        for j in range(i, n+1):
            augmented_matrix[i][j] = (augmented_matrix[i][j] * mod_inverse(pivot, p)) % p
        for j in range(n):
            if j != i:
                factor = augmented_matrix[j][i]
                for k in range(i, n+1):
                    augmented_matrix[j][k] = (augmented_matrix[j][k] - factor * augmented_matrix[i][k]) % p
    return [row[-1] for row in augmented_matrix]

def rank_of_matrix(A, p):
    n = len(A)
    A_copy = [row[:] for row in A]
    rank = 0
    for i in range(n):
        if A_copy[i][i]:
            rank += 1
            for j in range(i+1, n):
                factor = A_copy[j][i] * mod_inverse(A_copy[i][i], p) % p
                for k in range(i, n):
                    A_copy[j][k] = (A_copy[j][k] - factor * A_copy[i][k]) % p
    return rank

def generate_random_matroid(n, p):
    A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    while not is_independent_set(A, n, p):
        A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    return A

def is_independent_set(A, n, p):
    B = [A[i][:i] for i in range(n)]
    for i in range(n):
        if any(all(B[j][k] == A[i][k] for k in range(i)) for j in range(i)):
            return False
    return True

def simulate_protocol(A, n, p):
    rank = rank_of_matrix(A, p)
    communication_cost = 0
    # Simulate a simple protocol (e.g., brute-force) to estimate the communication cost
    # This is a placeholder and should be replaced with an actual protocol simulation
    for i in range(n):
        for j in range(i+1, n):
            if A[i][j] == 1:
                communication_cost += 1
    return communication_cost

def run_trial(seed: int) -> dict:
    random.seed(seed)
    p = 2
    n = 16
    instances_tested = 30
    total_communication_cost = 0
    rank_sum = 0
    
    for _ in range(instances_tested):
        A = generate_random_matroid(n, p)
        rank = rank_of_matrix(A, p)
        communication_cost = simulate_protocol(A, n, p)
        rank_sum += rank
        total_communication_cost += communication_cost
    
    mean_rank = rank_sum / instances_tested
    mean_communication_cost = total_communication_cost / instances_tested
    conjecture_holds = all(communication_cost >= rank * math.log2(n) for _ in range(instances_tested))
    
    return {
        "metric_name": "Communication Cost",
        "metric_value": mean_communication_cost,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(sys.argv[1])] if len(sys.argv) > 1 else [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")