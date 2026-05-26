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

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    augmented = [row + [b[i]] for i, row in enumerate(A)]
    for i in range(m):
        pivot_row = max(range(i, m), key=lambda r: abs(augmented[r][i]))
        if augmented[pivot_row][i] == 0:
            return None
        augmented[i], augmented[pivot_row] = augmented[pivot_row], augmented[i]
        for j in range(n + 1):
            if i != j:
                factor = augmented[j][i] / augmented[i][i]
                for k in range(i, n + 1):
                    augmented[j][k] -= factor * augmented[i][k]
    return [row[-1] for row in augmented]

def rank(matrix):
    A = matrix[:]
    m, n = len(A), len(A[0])
    r = 0
    for i in range(n):
        if r < m:
            pivot_row = max(range(r, m), key=lambda r: abs(A[r][i]))
            if A[pivot_row][i] == 0:
                continue
            A[r], A[pivot_row] = A[pivot_row], A[r]
            for j in range(m):
                if j != r:
                    factor = A[j][i] / A[r][i]
                    for k in range(n):
                        A[j][k] -= factor * A[r][k]
            r += 1
    return r

def generate_monotone_circuit(k, n):
    # Simplified representation of a monotone circuit computing k-CLIQUE
    circuit = []
    for _ in range(k):
        gate = random.choice(['AND', 'OR'])
        inputs = [random.randint(0, 1) for _ in range(n)]
        circuit.append((gate, inputs))
    return circuit

def quandle_representation(circuit):
    # Simplified representation of the quandle structure
    quandle = {}
    for gate, inputs in circuit:
        if gate == 'AND':
            key = tuple(sorted(inputs))
            if key not in quandle:
                quandle[key] = 1
            else:
                quandle[key] += 1
        elif gate == 'OR':
            key = tuple(sorted(inputs))
            if key not in quandle:
                quandle[key] = 0
            else:
                quandle[key] = max(quandle[key], 1)
    return list(quandle.values())

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            k = random.randint(1, min(n // 2, 4))
            circuit = generate_monotone_circuit(k, n)
            quandle_rep = quandle_representation(circuit)
            rank_quandle = rank(quandle_rep)
            
            if rank_quandle < 2**k:
                return {
                    "metric_name": "minimal_rank",
                    "metric_value": rank_quandle,
                    "instances_tested": 1,
                    "conjecture_holds": False,
                    "counterexample": f"n={n}, k={k}, rank={rank_quandle}, expected>=2^{k}"
                }
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": sum(results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        if not trial_result["conjecture_holds"]:
            print("RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed=<s>")
            sys.exit(0)
        results.append(trial_result["metric_value"])
    
    mean_value = sum(results) / len(results)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in results) / len(results))
    support_fraction = len([r for r in results if r >= 2**k]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction")