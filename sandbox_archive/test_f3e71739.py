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
    n = len(A)
    C = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    n = len(A)
    augmented = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(augmented[j][i]) > abs(augmented[max_row][i]):
                max_row = j
        augmented[i], augmented[max_row] = augmented[max_row], augmented[i]
        pivot = augmented[i][i]
        for j in range(i, n + 1):
            augmented[i][j] /= pivot
        for j in range(n):
            if j != i:
                factor = augmented[j][i]
                for k in range(i, n + 1):
                    augmented[j][k] -= factor * augmented[i][k]
    return [row[-1] for row in augmented]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_xor_and_network(n):
        inputs = [random.randint(0, 1) for _ in range(n)]
        gates = []
        for i in range(n-1):
            gate_type = random.choice(['XOR', 'AND'])
            if gate_type == 'XOR':
                gates.append((i, i+1))
            else:
                gates.append((i, i+1))
        return inputs, gates
    
    def compute_quandle_rank(gates):
        n = len(gates) + 1
        A = [[0 for _ in range(n)] for _ in range(n)]
        b = [0] * n
        for u, v in gates:
            A[u][v] += 1
            A[v][u] += 1
            b[u] -= 1
            b[v] -= 1
        rank = len(gaussian_elimination(A, b))
        return rank
    
    def compute_acc0_circuit_size(gates):
        n = len(gates) + 1
        size = 0
        for u, v in gates:
            if u < v:
                size += 2
            else:
                size += 3
        return size
    
    n = random.randint(5, 40)
    inputs, gates = generate_xor_and_network(n)
    quandle_rank = compute_quandle_rank(gates)
    acc0_circuit_size = compute_acc0_circuit_size(gates)
    
    metric_name = "Quandle Rank / ACC-0 Circuit Size"
    metric_value = quandle_rank / acc0_circuit_size
    instances_tested = 1
    conjecture_holds = quandle_rank <= math.log2(n) ** 2 and acc0_circuit_size <= math.log2(n) ** 2
    counterexample = "" if conjecture_holds else f"Quandle rank {quandle_rank} > log^2({n}) or ACC-0 circuit size {acc0_circuit_size} > log^2({n})"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")