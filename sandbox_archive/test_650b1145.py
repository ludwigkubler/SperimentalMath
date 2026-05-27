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
    m, k = len(A), len(B[0])
    n = len(B)
    C = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(n):
                C[i][j] += A[i][l] * B[l][j]
    return C

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i
        for k in range(i + 1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for k in range(i + 1, n):
            factor = A[k][i] / A[i][i]
            for j in range(i, n):
                A[k][j] -= factor * A[i][j]
            b[k] -= factor * b[i]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_circuit(n):
        circuit = []
        for _ in range(2 ** (n - 1)):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(n)]
            circuit.append((gate_type, inputs))
        return circuit
    
    def evaluate_circuit(circuit):
        stack = []
        for gate_type, inputs in reversed(circuit):
            if gate_type == 'AND':
                result = all(stack.pop() for _ in range(len(inputs)))
            elif gate_type == 'OR':
                result = any(stack.pop() for _ in range(len(inputs)))
            stack.append(result)
        return stack[0]
    
    def tropicalize_quiver(circuit):
        n = len(circuit[0][1])
        quiver = [[0] * n for _ in range(n)]
        for gate_type, inputs in circuit:
            if gate_type == 'AND':
                for i in range(n):
                    if inputs[i]:
                        quiver[i][i] += 1
                    else:
                        quiver[i][i] -= 1
            elif gate_type == 'OR':
                for i in range(n):
                    if inputs[i]:
                        quiver[i][i] += 1
        return quiver
    
    def minimal_rank(quiver):
        n = len(quiver)
        A = [[quiver[i][j] for j in range(n)] for i in range(n)]
        b = [0] * n
        try:
            x = gaussian_elimination(A, b)
            rank = sum(1 for val in x if abs(val) > 1e-9)
            return rank
        except Exception as e:
            return float('inf')
    
    def monotonicity_degree(circuit):
        n = len(circuit[0][1])
        degree = 0
        for gate_type, inputs in circuit:
            if gate_type == 'AND':
                degree += sum(1 for i in range(n) if inputs[i])
            elif gate_type == 'OR':
                degree += sum(1 for i in range(n) if not inputs[i])
        return degree
    
    n = random.randint(5, 40)
    circuit = generate_boolean_circuit(n)
    monotonicity = monotonicity_degree(circuit)
    quiver = tropicalize_quiver(circuit)
    rank = minimal_rank(quiver)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= monotonicity,
        "counterexample": "" if rank <= monotonicity else f"Monotonicity degree {monotonicity}, but minimal rank {rank}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(res["conjecture_holds"] for res in results):
        mean_rank = sum(res["metric_value"] for res in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        counterexample_desc = next(res["counterexample"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")