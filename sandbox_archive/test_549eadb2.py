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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError('Modular inverse does not exist')
    else:
        return x % m

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
    Augmented = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(Augmented[j][i]) > abs(Augmented[max_row][i]):
                max_row = j
        Augmented[i], Augmented[max_row] = Augmented[max_row], Augmented[i]
        pivot = Augmented[i][i]
        for j in range(i, n+1):
            Augmented[i][j] /= pivot
        for j in range(n):
            if j != i:
                factor = Augmented[j][i]
                for k in range(i, n+1):
                    Augmented[j][k] -= factor * Augmented[i][k]
    return [row[-1] for row in Augmented]

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    elif n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    else:
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det

def rank(A):
    n, m = len(A), len(A[0])
    Augmented = [A[i] + [1 if i == j else 0 for j in range(m)] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(Augmented[j][i]) > abs(Augmented[max_row][i]):
                max_row = j
        Augmented[i], Augmented[max_row] = Augmented[max_row], Augmented[i]
        pivot = Augmented[i][i]
        for j in range(i, m+1):
            Augmented[i][j] /= pivot
        for j in range(n):
            if j != i:
                factor = Augmented[j][i]
                for k in range(i, m+1):
                    Augmented[j][k] -= factor * Augmented[i][k]
    return sum(1 for row in Augmented if any(row[i] != 0 for i in range(m)))

def tropical_hodge_rank(M):
    n = len(M)
    identity = [[Fraction(1, 1) if i == j else Fraction(-math.inf, 1) for j in range(n)] for i in range(n)]
    result = identity
    for row in M:
        max_row = [max(row[j], result[i][j]) for j in range(n)]
        result = [[max(max_row[j], result[i][j]), max(max_row[k], result[i][k])] for i, k in [(i, j) for i in range(n) for j in range(i+1, n)]]
    return sum(1 for row in result if any(row[i] != Fraction(-math.inf, 1) for i in range(n)))

def generate_d_regular_circuit(d, n):
    circuit = []
    for _ in range(n-1):
        inputs = random.sample(range(n), d)
        output = random.choice(inputs)
        circuit.append((inputs, output))
    return circuit

def construct_matroid(circuit):
    matroid = set()
    for inputs, output in circuit:
        matroid.update(inputs)
    return matroid

def generate_instance(literals, clauses):
    instance = []
    for _ in range(clauses):
        clause = random.sample(literals, literals)
        instance.append(clause)
    return instance

def construct_matroid_from_instance(instance):
    matroid = set()
    for clause in instance:
        matroid.update(clause)
    return matroid

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    th_C_values = []
    C_sizes = []
    M_phi_sizes = []
    n_l_phi_values = []

    for n in n_values:
        circuit = generate_d_regular_circuit(2, n)
        matroid_C = construct_matroid(circuit)
        th_C = tropical_hodge_rank(matroid_C)
        th_C_values.append(th_C)
        C_sizes.append(len(circuit))

        if len(instance) >= 10 and max(len(clause) for clause in instance) > 6:
            M_phi = construct_matroid_from_instance(instance)
            M_phi_sizes.append(len(M_phi))
            n_l_phi_values.append(max(len(clause) for clause in instance))

    correlation_coefficient = sum((th_C - sum(th_C_values)/len(th_C_values)) * (C_size - sum(C_sizes)/len(C_sizes)) for th_C, C_size in zip(th_C_values, C_sizes)) / (sum((th_C - sum(th_C_values)/len(th_C_values))**2 for th_C in th_C_values) * sum((C_size - sum(C_sizes)/len(C_sizes))**2 for C_size in C_sizes)**0.5)

    conjecture_holds = correlation_coefficient >= 0.8 and all(M_phi_size >= n_l_phi_value**3 for M_phi_size, n_l_phi_value in zip(M_phi_sizes, n_l_phi_values))

    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = (sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))**0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")