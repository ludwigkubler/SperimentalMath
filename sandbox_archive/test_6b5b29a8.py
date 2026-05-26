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
        raise ValueError(f"No modular inverse for {a} modulo {m}")
    return x % m

def gaussian_elimination(A, b):
    n = len(b)
    A_augmented = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = max(range(i, n), key=lambda r: abs(A_augmented[r][i]))
        A_augmented[i], A_augmented[max_row] = A_augmented[max_row], A_augmented[i]
        factor = A_augmented[i][i]
        for j in range(i, n + 1):
            A_augmented[i][j] /= factor
        for k in range(n):
            if k != i:
                factor = A_augmented[k][i]
                for j in range(i, n + 1):
                    A_augmented[k][j] -= factor * A_augmented[i][j]
    return [row[-1] for row in A_augmented]

def dnf_to_matrix(dnf):
    n = len(dnf)
    m = max(len(clause) for clause in dnf)
    matrix = [[0] * m for _ in range(n)]
    for i, clause in enumerate(dnf):
        for literal in clause:
            if literal > 0:
                matrix[i][literal - 1] = 1
            else:
                matrix[i][-literal - 1] = 1
    return matrix

def rank(matrix):
    n, m = len(matrix), len(matrix[0])
    A = [row[:] for row in matrix]
    r = 0
    for j in range(m):
        i_max = next((i for i in range(r, n) if A[i][j]), None)
        if i_max is not None:
            A[r], A[i_max] = A[i_max], A[r]
            for i in range(r + 1, n):
                factor = A[i][j] / A[r][j]
                for k in range(m):
                    A[i][k] -= factor * A[r][k]
            r += 1
    return r

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_dnf(n, k):
        clauses = []
        for _ in range(k):
            clause = set()
            while len(clause) < n:
                literal = random.randint(1, 2 * n)
                if literal > n and -literal not in clause:
                    clause.add(-literal)
                elif literal <= n and literal not in clause:
                    clause.add(literal)
            clauses.append(list(clause))
        return clauses
    
    def circuit_size(dnf):
        n = len(dnf)
        m = max(len(clause) for clause in dnf)
        matrix = dnf_to_matrix(dnf)
        rank_val = rank(matrix)
        return n - rank_val + 1
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        dnf = generate_dnf(n, n // 2)
        matroid_rank = rank(dnf_to_matrix(dnf))
        circuit_size_val = circuit_size(dnf)
        results.append({
            "n": n,
            "matroid_rank": matroid_rank,
            "circuit_size": circuit_size_val
        })
    
    if not results:
        return {
            "metric_name": "Matroid Rank vs Circuit Size",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    matroid_ranks = [res["matroid_rank"] for res in results]
    circuit_sizes = [res["circuit_size"] for res in results]
    
    mean_matroid_rank = sum(matroid_ranks) / len(matroid_ranks)
    std_dev_matroid_rank = math.sqrt(sum((x - mean_matroid_rank) ** 2 for x in matroid_ranks) / len(matroid_ranks))
    correlation_coefficient = sum((matroid_ranks[i] - mean_matroid_rank) * (circuit_sizes[i] - sum(circuit_sizes) / len(circuit_sizes)) for i in range(len(matroid_ranks))) / (len(matroid_ranks) * std_dev_matroid_rank * math.sqrt(sum((x - sum(circuit_sizes) / len(circuit_sizes)) ** 2 for x in circuit_sizes)))
    
    conjecture_holds = correlation_coefficient > 0.5
    counterexample = "" if conjecture_holds else "Correlation coefficient below threshold"
    
    return {
        "metric_name": "Matroid Rank vs Circuit Size",
        "metric_value": mean_matroid_rank,
        "instances_tested": len(matroid_ranks),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_dev_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient below threshold\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE Reason=No instances generated")