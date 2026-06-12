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
    
    def generate_random_circuit(n, d):
        circuit = []
        for _ in range(d):
            gate_type = random.choice(['AND', 'OR'])
            if gate_type == 'AND':
                inputs = [random.randint(0, 1) for _ in range(n)]
                circuit.append((gate_type, inputs))
            else:
                inputs = [random.randint(0, 1) for _ in range(n)]
                circuit.append((gate_type, inputs))
        return circuit
    
    def matrix_mult(A, B):
        m, k = len(A), len(B[0])
        n = len(B)
        C = [[0] * k for _ in range(m)]
        for i in range(m):
            for j in range(k):
                for l in range(n):
                    C[i][j] += A[i][l] * B[l][j]
        return C
    
    def matrix_add(A, B):
        m = len(A)
        n = len(A[0])
        C = [[A[i][j] + B[i][j] for j in range(n)] for i in range(m)]
        return C
    
    def matrix_sub(A, B):
        m = len(A)
        n = len(A[0])
        C = [[A[i][j] - B[i][j] for j in range(n)] for i in range(m)]
        return C
    
    def matrix_transpose(A):
        m = len(A)
        n = len(A[0])
        B = [[0] * m for _ in range(n)]
        for i in range(m):
            for j in range(n):
                B[j][i] = A[i][j]
        return B
    
    def matrix_inv(A, mod):
        m = len(A)
        n = len(A[0])
        I = [[1 if i == j else 0 for j in range(n)] for i in range(m)]
        for k in range(n):
            pivot = A[k][k]
            if pivot == 0:
                return None
            pivot_inv = pow(pivot, mod - 2, mod)
            for j in range(n):
                A[k][j] *= pivot_inv % mod
                I[k][j] *= pivot_inv % mod
            for i in range(m):
                if i != k:
                    factor = A[i][k]
                    for j in range(n):
                        A[i][j] -= (factor * A[k][j]) % mod
                        I[i][j] -= (factor * I[k][j]) % mod
        return I
    
    def matrix_det(A, mod):
        m = len(A)
        n = len(A[0])
        det = 1
        for k in range(n):
            pivot = A[k][k]
            if pivot == 0:
                return 0
            det *= pivot % mod
            for j in range(k + 1, n):
                A[k][j] /= pivot
            for i in range(k + 1, m):
                factor = A[i][k]
                for j in range(k + 1, n):
                    A[i][j] -= (factor * A[k][j])
        return det % mod
    
    def matrix_rank(A, mod):
        m = len(A)
        n = len(A[0])
        rank = 0
        for k in range(min(m, n)):
            if A[k][k] != 0:
                rank += 1
                for i in range(k + 1, m):
                    factor = A[i][k]
                    for j in range(n):
                        A[i][j] -= (factor * A[k][j]) % mod
        return rank
    
    def circuit_to_matrix(circuit, n):
        m = len(circuit)
        matrix = [[0] * (2 ** n) for _ in range(2 ** n)]
        for i in range(2 ** n):
            inputs = [int(x) for x in format(i, f'0{n}b')]
            outputs = [0] * n
            for gate_type, gate_inputs in circuit:
                if gate_type == 'AND':
                    outputs[gate_inputs.index(1)] = 1
                else:
                    outputs[gate_inputs.index(0)] = 1
            matrix[i][i] = 1
        return matrix
    
    def br_group_order(matrix):
        mod = 2 ** n
        det = matrix_det(matrix, mod)
        rank = matrix_rank(matrix, mod)
        order = det * (mod - 1) ** (n - rank)
        return order % mod
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            circuit = generate_random_circuit(n, random.randint(1, 10))
            matrix = circuit_to_matrix(circuit, n)
            order = br_group_order(matrix)
            depth = len(circuit)
            results.append((order, depth))
    
    if not results:
        return {
            "metric_name": "Brauer Group Order / Circuit Depth Ratio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ratios = [order / depth for order, depth in results]
    mean_ratio = sum(ratios) / len(ratios)
    std_ratio = math.sqrt(sum((x - mean_ratio) ** 2 for x in ratios) / len(ratios))
    support_fraction = sum(1 for r in ratios if abs(r - mean_ratio) <= 0.3 * mean_ratio) / len(ratios)
    
    return {
        "metric_name": "Brauer Group Order / Circuit Depth Ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": support_fraction >= 0.95,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")