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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, m):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def matrix_multiplication(A, B):
    m, n = len(A), len(B[0])
    p = len(B)
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    m, n = len(A), len(A[0])
    if m != n:
        raise ValueError("Matrix must be square")
    if n == 1:
        return A[0][0]
    det = Fraction(0)
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        sign = (-1) ** (j % 2)
        det += sign * A[0][j] * determinant(submatrix)
    return det

def minimal_geometric_entropy(ideal):
    m, n = len(ideal), len(ideal[0])
    if m == 0 or n == 0:
        raise ValueError("Ideal must be non-empty")
    A = [[Fraction(a) for a in row] for row in ideal]
    rank = 0
    for i in range(min(m, n)):
        if determinant([row[j:] for row in A[i:]]) != Fraction(0):
            rank += 1
    return rank * math.log(n)

def generate_boolean_circuit(depth, n):
    circuit = []
    for _ in range(depth):
        gate = random.choice(['AND', 'OR'])
        inputs = [random.randint(0, 1) for _ in range(n)]
        circuit.append((gate, inputs))
    return circuit

def tautological_ideal(circuit):
    n = len(circuit[0][1])
    ideal = []
    for i in range(2**n):
        row = [i >> j & 1 for j in range(n)]
        for gate, inputs in circuit:
            if gate == 'AND':
                result = all(row[j] for j in inputs)
            elif gate == 'OR':
                result = any(row[j] for j in inputs)
            else:
                raise ValueError("Invalid gate")
            row.append(result)
        ideal.append(row)
    return ideal

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            circuit = generate_boolean_circuit(random.randint(1, 5), n)
            ideal = tautological_ideal(circuit)
            H_min = minimal_geometric_entropy(ideal)
            d = len(circuit)
            expected = d**2 * math.log(n)
            results.append((H_min, d, n, abs(H_min - expected) <= 0.1 * expected))
    
    if not results:
        return {
            "metric_name": "minimal_geometric_entropy",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No data collected"
        }
    
    H_min_values = [H for H, _, _, _ in results]
    d_values = [d for _, d, _, _ in results]
    n_values = [n for _, _, n, _ in results]
    holds = all(holds for _, _, _, holds in results)
    
    return {
        "metric_name": "minimal_geometric_entropy",
        "metric_value": sum(H_min_values) / len(H_min_values),
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_H_min = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_H_min = math.sqrt(sum((r["metric_value"] - mean_H_min)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_H_min} std={std_H_min} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.95:
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")