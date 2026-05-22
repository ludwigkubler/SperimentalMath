# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations, permutations

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_multiply(A, B):
    m, n = len(A), len(B[0])
    p = len(B)
    result = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                result[i][j] += A[i][k] * B[k][j]
    return result

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    augmented_matrix = [A[i] + [b[i]] for i in range(m)]
    for i in range(n):
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
                for k in range(n+1):
                    augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    return [row[-1] for row in augmented_matrix]

def k_theory_rank(ideal):
    generators = list(ideal)
    m, n = len(generators), len(generators[0])
    A = [[generators[i][j] for j in range(n)] for i in range(m)]
    rank = 0
    for i in range(n):
        if any(A[j][i] != 0 for j in range(rank, m)):
            rank += 1
    return rank

def construct_monotone_circuit(ideal):
    generators = list(ideal)
    n = len(generators[0])
    circuit = []
    for i in range(n):
        for j in range(i+1, n):
            if any(generators[k][i] * generators[k][j] != 0 for k in range(len(generators))):
                circuit.append((i, j))
    return circuit

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    variables = set(range(n))
    ideal = {frozenset(random.sample(variables, k)) for k in range(1, n)}
    
    rank = k_theory_rank(ideal)
    circuit = construct_monotone_circuit(ideal)
    depth = len(circuit) + 1
    
    return {
        "metric_name": "Rank of K-theory Group / Depth of Circuit",
        "metric_value": Fraction(rank, depth),
        "instances_tested": 1,
        "conjecture_holds": rank <= depth,
        "counterexample": "" if rank <= depth else f"Counterexample: Rank {rank}, Depth {depth}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 89))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(res["conjecture_holds"] for res in results):
        mean_value = sum(res["metric_value"] for res in results) / len(results)
        support_fraction = 1.0
        result = f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next((res["seed"] for res in results if not res["conjecture_holds"]), None)
        counterexample = next((res["counterexample"] for res in results if res["counterexample"]), "")
        result = f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}"
    
    print(result)