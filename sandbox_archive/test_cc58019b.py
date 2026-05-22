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
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = 1 / A[i][i]
            for j in range(i, n):
                A[i][j] *= factor
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(i, n):
                        A[k][j] -= factor * A[i][j]
        return A
    
    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def symplectic_form(A, B):
        n = len(A)
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        return matrix_multiply(matrix_multiply(B, A), I) - matrix_multiply(I, matrix_multiply(A, B))
    
    def minimal_rank(A):
        rank = 0
        A_rref = gaussian_elimination(A)
        for row in A_rref:
            if any(row[i] != 0 for i in range(len(row))):
                rank += 1
        return rank
    
    def generate_ac0_circuit(n, max_gates):
        gates = ['NOT', 'XOR']
        circuit = []
        for _ in range(max_gates):
            gate = random.choice(gates)
            inputs = [random.randint(0, 1) for _ in range(random.randint(1, n))]
            circuit.append((gate, inputs))
        return circuit
    
    def construct_algebra(circuit):
        n = len(circuit)
        A = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                if bin(i).count('1') + bin(j).count('1') <= n:
                    A[i][j] = 1
        return A
    
    def gate_count(circuit):
        return len(circuit)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    circuit = generate_ac0_circuit(n, max_gates=40)
    A = construct_algebra(circuit)
    rank = minimal_rank(A)
    
    return {
        "metric_name": "gate_count",
        "metric_value": gate_count(circuit),
        "instances_tested": 1,
        "conjecture_holds": rank == gate_count(circuit),
        "counterexample": "" if rank == gate_count(circuit) else f"Gate count mismatch: {rank} != {gate_count(circuit)}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")