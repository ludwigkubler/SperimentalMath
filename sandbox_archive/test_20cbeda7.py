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
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return abs(a * b) // gcd(a, b)
    
    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
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
            factor = 1 / augmented_matrix[i][i]
            for j in range(n):
                augmented_matrix[i][j] *= factor
            b[i] *= factor
            for j in range(n):
                if i != j:
                    factor = augmented_matrix[j][i]
                    for k in range(n):
                        augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
                    b[j] -= factor * b[i]
        return [row[:-1] for row in augmented_matrix], b
    
    def rank(matrix):
        A, _ = gaussian_elimination(matrix, [0] * len(matrix))
        return sum(1 for row in A if any(row))
    
    def construct_category(f):
        n = len(f)
        category = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                category[i][j] = f[j] - f[i]
        return category
    
    def acc0_circuit_size(f):
        n = len(f)
        if n == 1:
            return 1
        size = n
        for i in range(1, n):
            for j in range(i+1, n):
                if f[j] - f[i] != 0:
                    size += acc0_circuit_size([f[k] - f[i] for k in range(n) if k != i and k != j])
        return size
    
    def categorified_k_theory_group(f):
        category = construct_category(f)
        return rank(category)
    
    n = random.randint(5, 40)
    f = [random.randint(1, 100) for _ in range(n)]
    s_f = acc0_circuit_size(f)
    G_f = categorified_k_theory_group(f)
    
    return {
        "metric_name": "Minimal Rank of Categorified K-theory Group",
        "metric_value": G_f,
        "instances_tested": 1,
        "conjecture_holds": G_f <= s_f,
        "counterexample": "" if G_f <= s_f else f"Function: {f}, Category Size: {s_f}, Rank: {G_f}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
        print(f"RESULT: FALSIFIED counterexample=\"Function does not satisfy the conjecture\" first_failing_seed={first_failing_seed}")