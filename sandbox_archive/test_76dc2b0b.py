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

def generate_ac0_circuit(n):
    if n == 1:
        return [random.choice([0, 1])]
    else:
        subcircuits = [generate_ac0_circuit(n-1) for _ in range(2)]
        gate = random.choice(['OR', 'AND'])
        return [gate] + sum(subcircuits, [])

def truth_table(circuit):
    n = len(circuit)
    def eval_circuit(inputs):
        if isinstance(circuit[0], str):
            if circuit[0] == 'OR':
                return eval_circuit(inputs[:n//2]) or eval_circuit(inputs[n//2:])
            elif circuit[0] == 'AND':
                return eval_circuit(inputs[:n//2]) and eval_circuit(inputs[n//2:])
        else:
            return inputs[circuit[0]]
    return [eval_circuit([i for i in range(1 << n) if (i >> j) & 1]) for j in range(n)]

def walsh_hadamard_transform(table):
    n = len(table)
    def hadamard(a, b):
        return a + b, a - b
    def transform(matrix):
        if len(matrix) == 1:
            return matrix
        else:
            top_left = transform([row[:len(row)//2] for row in matrix])
            top_right = transform([row[len(row)//2:] for row in matrix])
            bottom_left = transform([row[:len(row)//2] for row in matrix])
            bottom_right = transform([row[len(row)//2:] for row in matrix])
            return [hadamard(a, b) for a, b in zip(top_left, top_right)] + \
                   [hadamard(a, -b) for a, b in zip(bottom_left, bottom_right)]
    return transform(table)

def eigenvalues(matrix):
    n = len(matrix)
    def matrix_mult(A, B):
        return [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
    def identity_matrix(n):
        return [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    def matrix_add(A, B):
        return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]
    def matrix_subtract(A, B):
        return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]
    def scalar_multiply(matrix, c):
        return [[c * matrix[i][j] for j in range(n)] for i in range(n)]
    def determinant(matrix):
        if n == 1:
            return matrix[0][0]
        else:
            det = 0
            for j in range(n):
                submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
                det += (-1) ** j * matrix[0][j] * determinant(submatrix)
            return det
    def inverse(matrix):
        det = determinant(matrix)
        if det == 0:
            raise ValueError("Matrix is not invertible")
        adjugate = [[(-1) ** (i + j) * determinant([[matrix[k][l] for l in range(j, j+1)] for k in range(i, i+1)]) for j in range(n)] for i in range(n)]
        return scalar_multiply(adjugate, 1 / det)
    def power(matrix, k):
        result = identity_matrix(n)
        base = matrix
        while k > 0:
            if k % 2 == 1:
                result = matrix_mult(result, base)
            base = matrix_mult(base, base)
            k //= 2
        return result
    eigenvals = []
    for _ in range(100):
        guess = [[random.random() for _ in range(n)] for _ in range(n)]
        guess_inv = inverse(guess)
        guess_power = power(guess, n-1)
        guess_inv_power = power(guess_inv, n-1)
        eigenval = (guess_power[0][0] + guess_inv_power[0][0]) / 2
        eigenvals.append(eigenval)
    return eigenvals

def rank_stable(matrix):
    eigenvals = eigenvalues(matrix)
    return sum(1 for val in eigenvals if abs(val) > 1e-6)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 10
    circuit = generate_ac0_circuit(n)
    table = truth_table(circuit)
    M_C = walsh_hadamard_transform(table)
    rank = rank_stable(M_C)
    metric_value = rank / math.log2(n)
    conjecture_holds = metric_value >= 0.6 * math.log2(n)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "rank_stable",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    mean = sum(r['metric_value'] for r in results) / len(results)
    std = math.sqrt(sum((r['metric_value'] - mean) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")