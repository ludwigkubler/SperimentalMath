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
        return (b, 0, 1)
    else:
        g, x, y = extended_gcd(b % a, a)
        return (g, y - (b // a) * x, x)

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError("Inverse doesn't exist")
    else:
        return x % m

def matrix_multiply(A, B):
    n = len(A)
    C = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def matrix_power(A, n):
    result = [[1 if i == j else 0 for j in range(len(A))] for i in range(len(A))]
    while n > 0:
        if n % 2 == 1:
            result = matrix_multiply(result, A)
        A = matrix_multiply(A, A)
        n //= 2
    return result

def is_quasi_group(Q):
    n = len(Q)
    for a in range(n):
        for b in range(n):
            if Q[a][b] not in range(n):
                return False
    for a in range(n):
        for c in range(n):
            found = False
            for b in range(n):
                if Q[a][b] == c:
                    found = True
                    break
            if not found:
                return False
    for b in range(n):
        for c in range(n):
            found = False
            for a in range(n):
                if Q[a][b] == c:
                    found = True
                    break
            if not found:
                return False
    return True

def generate_acc0_circuit(n):
    if n == 1:
        return [[0]]
    else:
        circuits = []
        for i in range(2, n + 1):
            for j in range(i - 1):
                circuit = [[j] * (i - 1)]
                for k in range(j + 1, i):
                    circuit.append([k] * (i - 1))
                circuits.append(circuit)
        return random.choice(circuits)

def quasi_group_representation(C):
    n = len(C)
    Q = [[0 for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            Q[a][b] = C[b][a]
    return Q

def rank(matrix):
    m, n = len(matrix), len(matrix[0])
    augmented_matrix = [row + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(matrix)]
    for i in range(m):
        max_row = max(range(i, m), key=lambda r: abs(augmented_matrix[r][i]))
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        if augmented_matrix[i][i] == 0:
            return None
        for j in range(n + 1):
            augmented_matrix[i][j] /= augmented_matrix[i][i]
        for k in range(m):
            if k != i and augmented_matrix[k][i] != 0:
                factor = augmented_matrix[k][i]
                for j in range(n + 1):
                    augmented_matrix[k][j] -= factor * augmented_matrix[i][j]
    return sum(1 for row in augmented_matrix if any(abs(x) > 1e-9 for x in row[:n]))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        C = generate_acc0_circuit(n)
        Q = quasi_group_representation(C)
        if not is_quasi_group(Q):
            return {
                "metric_name": "rank",
                "metric_value": None,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        rank_Q = rank(Q)
        if rank_Q is None:
            continue
        results.append((n, rank_Q))
    
    mean_rank = sum(rank for _, rank in results) / len(results)
    std_dev = math.sqrt(sum((rank - mean_rank) ** 2 for _, rank in results) / len(results))
    support_fraction = len([r for _, r in results if abs(r - math.log(n)) <= 1]) / len(results)
    
    return {
        "metric_name": "rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"support_fraction={support_fraction}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results if r["instances_tested"] > 0) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results if r["instances_tested"] > 0) / len(results))
    support_fraction = sum(1 for r in results if 'conjecture_holds' in r and r['conjecture_holds']) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif any(r["instances_tested"] > 0 and not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r['seed'] for r in results if 'conjecture_holds' in r and not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"support_fraction={support_fraction}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction=<z>")