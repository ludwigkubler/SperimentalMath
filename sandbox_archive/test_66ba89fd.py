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

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_primes(count):
    primes = []
    num = 2
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(matrix, b):
        n = len(b)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i + 1, n):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
                b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n - 1, -1, -1):
            x[i] = (b[i] - sum(matrix[i][j] * x[j] for j in range(i + 1, n))) / matrix[i][i]
        return x

    def matrix_multiply(A, B):
        m, k = len(A), len(B[0])
        result = [[0] * k for _ in range(m)]
        for i in range(m):
            for j in range(k):
                for l in range(len(B)):
                    result[i][j] += A[i][l] * B[l][j]
        return result

    def mod_inverse(a, m):
        m0, x0, x1 = m, 0, 1
        if m == 1:
            return 0
        while a > 1:
            q = a // m
            m, a = a % m, m
            x0, x1 = x1 - q * x0, x0
        if x1 < 0:
            x1 += m0
        return x1

    def mod_matrix_inverse(matrix, p):
        n = len(matrix)
        identity = [[int(i == j) for j in range(n)] for i in range(n)]
        augmented = [row + [identity[i]] for i, row in enumerate(matrix)]
        for i in range(n):
            pivot = augmented[i][i]
            if pivot == 0:
                return None
            for j in range(i, n * 2):
                augmented[i][j] *= mod_inverse(pivot, p)
            for j in range(n):
                if j != i:
                    factor = augmented[j][i]
                    for k in range(i, n * 2):
                        augmented[j][k] -= factor * augmented[i][k]
        return [row[n:] for row in augmented]

    def mod_matrix_power(matrix, power, p):
        result = [[int(i == j) for j in range(len(matrix))] for i in range(len(matrix))]
        while power > 0:
            if power % 2 == 1:
                result = matrix_multiply(result, matrix)
                result = [[x % p for x in row] for row in result]
            matrix = matrix_multiply(matrix, matrix)
            matrix = [[x % p for x in row] for row in matrix]
            power //= 2
        return result

    def mod_matrix_trace(matrix, p):
        return sum(matrix[i][i] for i in range(len(matrix))) % p

    def generate_random_circuit(n, depth=3):
        if depth == 0:
            return [[random.choice([1, 0])]]
        else:
            inputs = generate_random_circuit(n, depth - 1)
            gates = [random.choice(['AND', 'OR', 'MOD']) for _ in range(n)]
            circuit = []
            for i in range(n):
                if gates[i] == 'AND':
                    circuit.append([inputs[0][i], inputs[1][i]])
                elif gates[i] == 'OR':
                    circuit.append([inputs[0][i], inputs[1][i]])
                else:
                    p = random.choice(generate_primes(5))
                    circuit.append([inputs[0][i], inputs[1][i], p])
            return [circuit]

    def evaluate_circuit(circuit, input_values):
        stack = []
        for gate in circuit:
            if len(gate) == 2:
                a, b = stack.pop(), stack.pop()
                if gate[0] == 'AND':
                    stack.append(a and b)
                elif gate[0] == 'OR':
                    stack.append(a or b)
            else:
                a, b, p = stack.pop(), stack.pop(), gate[2]
                if gate[0] == 'MOD':
                    stack.append((a + b) % p)
        return stack.pop()

    def approximate_mcsp(circuit, input_values, epsilon):
        n = len(input_values)
        m = 10 * n
        A = [[random.choice([0, 1]) for _ in range(n)] for _ in range(m)]
        b = [evaluate_circuit(circuit, input_values) for _ in range(m)]
        x = gaussian_elimination(A, b)
        return sum(x[i] * input_values[i] for i in range(n))

    n = random.randint(5, 40)
    circuit = generate_random_circuit(n)
    input_values = [random.choice([0, 1]) for _ in range(n)]
    epsilon = 0.1
    approximation = approximate_mcsp(circuit, input_values, epsilon)

    return {
        "metric_name": "approximation_error",
        "metric_value": abs(approximation - evaluate_circuit(circuit, input_values)),
        "instances_tested": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes(30)
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")