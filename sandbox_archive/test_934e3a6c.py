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

def isqrt(n):
    x = n
    y = (x + 1) // 2
    while y < x:
        x, y = y, (y + x) // 2
    return x

def qr_decomposition(A):
    m, n = len(A), len(A[0])
    Q = [[0] * n for _ in range(m)]
    R = [[A[i][j] if i == j else 0 for j in range(n)] for i in range(m)]
    
    for k in range(n):
        norm = sum(A[i][k]**2 for i in range(k, m))**0.5
        Q[k][k] = A[k][k] / norm
        R[0][k] = A[0][k]
        
        for j in range(k + 1, n):
            R[j][k] = sum(Q[i][k] * A[i][j] for i in range(k, m))
            Q[j][k] = sum(Q[k][i] * A[i][j] for i in range(k, m)) / norm
    
    return Q, R

def matrix_multiplication(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    
    return C

def real_rank(matrix):
    Q, R = qr_decomposition(matrix)
    rank = sum(1 for row in R if any(row[j] != 0 for j in range(len(row))))
    return rank

def generate_ac0_circuit(n):
    circuit = []
    for _ in range(n):
        gate = random.choice(['AND', 'OR'])
        inputs = [random.randint(0, 1) for _ in range(2)]
        circuit.append((gate, inputs))
    
    return circuit

def polynomial_representation(circuit):
    n = len(circuit)
    matrix = [[0] * (n + 1) for _ in range(n + 1)]
    
    for i in range(n):
        gate, inputs = circuit[i]
        if gate == 'AND':
            matrix[inputs[0]][i] += 1
            matrix[inputs[1]][i] += 1
            matrix[n][i] -= 2
        elif gate == 'OR':
            matrix[inputs[0]][i] += 1
            matrix[inputs[1]][i] += 1
            matrix[n][i] -= 1
    
    return matrix

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 40
    instances_tested = 30
    real_rank_threshold = 0.3 * math.log2(n)
    
    results = []
    for _ in range(instances_tested):
        circuit = generate_ac0_circuit(n)
        matrix = polynomial_representation(circuit)
        rank = real_rank(matrix)
        
        results.append(rank >= real_rank_threshold)
    
    conjecture_holds = all(results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "real_rank",
        "metric_value": sum(results) / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")