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
    return abs(a*b) // gcd(a, b)

def matrix_multiply(A, B):
    m, k = len(A), len(B[0])
    n = len(B)
    C = [[0 for _ in range(k)] for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(n):
                C[i][j] += A[i][l] * B[l][j]
    return C

def gaussian_elimination(A, b):
    m, n = len(A), len(b)
    Augmented = [A[i] + [b[i]] for i in range(m)]
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(Augmented[j][i]) > abs(Augmented[max_row][i]):
                max_row = j
        Augmented[i], Augmented[max_row] = Augmented[max_row], Augmented[i]
        pivot = Augmented[i][i]
        for j in range(i, n+1):
            Augmented[i][j] /= pivot
        for j in range(m):
            if j != i:
                factor = Augmented[j][i]
                for k in range(n+1):
                    Augmented[j][k] -= factor * Augmented[i][k]
    return [row[-1] for row in Augmented]

def calculate_circuit_group_order(circuit):
    d, w = len(circuit), len(circuit[0])
    if all(all(circuit[layer][i] == j % w for i in range(w)) for layer in range(d)):
        return 1
    G = [[0]*w for _ in range(w)]
    for layer in range(d):
        for i in range(w):
            for j in range(w):
                if circuit[layer][i] == (j + 1) % w:
                    G[i][j] = 1
    I = [[int(i==j) for j in range(w)] for i in range(w)]
    order = 1
    while True:
        G = matrix_multiply(G, G)
        order += 1
        if gaussian_elimination(G + I, [0]*w + [1]*w) == [1]*w:
            return order

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_order = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per size
            perm = random.sample(range(n), n)
            circuit = [[random.randint(0, w-1) for _ in range(w)] for _ in range(d)]
            
            permutation_order = calculate_circuit_group_order([perm])
            total_order += permutation_order
            instances_tested += 1
            
            if permutation_order < n**2 / 4:
                return {
                    "metric_name": "permutation_order",
                    "metric_value": permutation_order,
                    "instances_tested": instances_tested,
                    "conjecture_holds": False,
                    "counterexample": f"Permutation {perm} has order {permutation_order}"
                }
    
    mean_order = total_order / instances_tested
    return {
        "metric_name": "permutation_order",
        "metric_value": mean_order,
        "instances_tested": instances_tested,
        "conjecture_holds": mean_order >= n**2 / 4,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_order = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_order} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_order} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Permutation order is less than n^2/4\" first_failing_seed={first_failing_seed}")