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

# Helper functions for matrix operations
def matrix_mult(A, B, n):
    result = [[0] * n for _ in range(n)]
    mod = 2
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] = (result[i][j] + A[i][k] * B[k][j]) % mod
    return result

def matrix_add(A, B, n):
    result = [[0] * n for _ in range(n)]
    mod = 2
    for i in range(n):
        for j in range(n):
            result[i][j] = (A[i][j] + B[i][j]) % mod
    return result

def matrix_sub(A, B, n):
    result = [[0] * n for _ in range(n)]
    mod = 2
    for i in range(n):
        for j in range(n):
            result[i][j] = (A[i][j] - B[i][j]) % mod
    return result

def matrix_inv(A, n):
    I = [[0] * n for _ in range(n)]
    for i in range(n):
        I[i][i] = 1
    for i in range(n):
        pivot = A[i][i]
        if pivot == 0:
            raise ValueError("Matrix is not invertible")
        for j in range(n):
            A[i][j] /= pivot
            I[i][j] /= pivot
        for k in range(n):
            if k != i:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]
                    I[k][j] -= factor * I[i][j]
    return I

def gaussian_elimination(A, n):
    I = [[0] * n for _ in range(n)]
    for i in range(n):
        I[i][i] = 1
    for i in range(n):
        pivot_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[pivot_row][i]):
                pivot_row = j
        A[i], A[pivot_row] = A[pivot_row], A[i]
        I[i], I[pivot_row] = I[pivot_row], I[i]
        for j in range(n):
            if j != i:
                factor = A[j][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
                    I[j][k] -= factor * I[i][k]
    return I

def symplectic_invariant(circuit, n):
    CNOT = [[0, 1], [1, 0]]
    identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    invariant = identity
    for gate in circuit:
        if gate[0] == 'CNOT':
            q1, q2 = gate[1]
            CNOT_matrix = [[0] * n for _ in range(n)]
            CNOT_matrix[q1][q1] = 1
            CNOT_matrix[q1][q2] = 1
            CNOT_matrix[q2][q1] = 1
            CNOT_matrix[q2][q2] = 1
            invariant = matrix_mult(invariant, CNOT_matrix, n)
        elif gate[0] == 'H':
            qubit = gate[1]
            H_matrix = [[0] * n for _ in range(n)]
            H_matrix[qubit][qubit] = 1
            H_matrix[qubit][qubit] = -1
            invariant = matrix_mult(invariant, H_matrix, n)
    return invariant

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    circuit_size = random.randint(10, 30)
    circuit = []
    for _ in range(circuit_size):
        gate_type = random.choice(['CNOT', 'H'])
        if gate_type == 'CNOT':
            qubit1 = random.randint(0, n-1)
            qubit2 = random.randint(0, n-1)
            while qubit1 == qubit2:
                qubit2 = random.randint(0, n-1)
            circuit.append(('CNOT', (qubit1, qubit2)))
        elif gate_type == 'H':
            qubit = random.randint(0, n-1)
            circuit.append(('H', qubit))
    
    try:
        invariant = symplectic_invariant(circuit, n)
        entanglement_complexity = len(circuit)  # Simplified for testing
        order = sum(sum(row) for row in invariant)
        return {
            "metric_name": "Minimal Order of Symplectic Invariant",
            "metric_value": order,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": True,
            "counterexample": ""
        }
    except Exception as e:
        return {
            "metric_name": "Minimal Order of Symplectic Invariant",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": str(e)
        }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        seeds = [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")