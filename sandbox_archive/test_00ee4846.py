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
    
    def generate_boolean_circuit(depth):
        if depth == 0:
            return ['0', '1']
        else:
            inputs = generate_boolean_circuit(depth - 1)
            outputs = []
            for i in range(len(inputs)):
                for j in range(i + 1, len(inputs)):
                    outputs.append(f"({inputs[i]} & {inputs[j]})")
                    outputs.append(f"({inputs[i]} | {inputs[j]})")
                    outputs.append(f"(~{inputs[i]})")
                    outputs.append(f"(~{inputs[j]})")
            return outputs
    
    def matrix_multiply(A, B):
        n = len(A)
        C = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def matrix_add(A, B):
        n = len(A)
        C = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                C[i][j] = A[i][j] + B[i][j]
        return C
    
    def matrix_sub(A, B):
        n = len(A)
        C = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                C[i][j] = A[i][j] - B[i][j]
        return C
    
    def matrix_transpose(A):
        n = len(A)
        T = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                T[j][i] = A[i][j]
        return T
    
    def matrix_inverse(A, mod):
        n = len(A)
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        for k in range(n):
            pivot = A[k][k]
            for j in range(n):
                A[k][j] = (A[k][j] * pow(pivot, -1, mod)) % mod
                I[k][j] = (I[k][j] * pow(pivot, -1, mod)) % mod
            for i in range(n):
                if i != k:
                    factor = A[i][k]
                    for j in range(n):
                        A[i][j] = (A[i][j] - factor * A[k][j]) % mod
                        I[i][j] = (I[i][j] - factor * I[k][j]) % mod
        return I
    
    def matrix_power(A, k, mod):
        n = len(A)
        result = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            result[i][i] = 1
        while k > 0:
            if k % 2 == 1:
                result = matrix_multiply(result, A, mod)
            A = matrix_multiply(A, A, mod)
            k //= 2
        return result
    
    def matrix_determinant(A):
        n = len(A)
        det = 0
        for i in range(n):
            submatrix = [row[:i] + row[i+1:] for row in A[1:]]
            sign = (-1) ** i
            det += sign * A[0][i] * matrix_determinant(submatrix)
        return det
    
    def gaussian_elimination(A, b):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            pivot = A[i][i]
            for j in range(i, n):
                A[i][j] /= pivot
            b[i] /= pivot
            for j in range(n):
                if j != i:
                    factor = A[j][i]
                    for k in range(i, n):
                        A[j][k] -= factor * A[i][k]
                    b[j] -= factor * b[i]
        return [b[i] for i in range(n)]
    
    def matrix_rank(A):
        n = len(A)
        rank = 0
        for i in range(n):
            if all(A[j][i] == 0 for j in range(rank)):
                continue
            rank += 1
        return rank
    
    def circuit_to_matrix(circuit, n):
        A = [[0 for _ in range(2**n)] for _ in range(2**n)]
        b = [0 for _ in range(2**n)]
        for expr in circuit:
            if expr == '0':
                b[0] += 1
            elif expr == '1':
                b[1] += 1
            else:
                i, j = int(expr[1]), int(expr[3])
                A[i][j] += 1
                A[j][i] += 1
        return A, b
    
    def minimal_brauer_group_order(A):
        n = len(A)
        det = matrix_determinant(A)
        if det == 0:
            return 0
        rank = matrix_rank(A)
        return det ** (n - rank)
    
    def circuit_depth(circuit):
        max_depth = 0
        for expr in circuit:
            depth = 0
            while '(' in expr:
                expr = expr.replace('(', '').replace(')', '')
                depth += 1
            if depth > max_depth:
                max_depth = depth
        return max_depth
    
    n_max = 5
    instances_tested = 0
    total_ratio = 0
    
    for _ in range(30):
        depth = random.randint(2, n_max)
        circuit = generate_boolean_circuit(depth)
        A, b = circuit_to_matrix(circuit, len(circuit))
        br_order = minimal_brauer_group_order(A)
        d_C = circuit_depth(circuit)
        
        if br_order == 0 or d_C == 0:
            continue
        
        ratio = br_order / d_C
        total_ratio += ratio
        instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "ratio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_ratio = total_ratio / instances_tested
    std_ratio = (sum((ratio - mean_ratio) ** 2 for ratio in range(instances_tested)) / instances_tested) ** 0.5
    
    return {
        "metric_name": "ratio",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(mean_ratio - 1) <= 0.3,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_ratio = (sum((r["metric_value"] - mean_ratio) ** 2 for r in results if r["metric_value"] is not None) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")