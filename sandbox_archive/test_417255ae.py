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
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        factor = Fraction(A[i][i])
        for j in range(n):
            A[i][j] /= factor
        for j in range(n):
            if i != j:
                factor = Fraction(A[j][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]

def matrix_multiplication(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def min_eigenform_order(A):
    n = len(A)
    identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    gaussian_elimination(A)
    order = 1
    while True:
        product = matrix_multiplication(A, A)
        if product == identity:
            return order
        order += 1

def generate_boolean_circuit(size):
    n = size
    circuit = []
    for _ in range(n):
        gate = random.choice(['AND', 'OR'])
        inputs = [random.randint(0, 1) for _ in range(2)]
        circuit.append((gate, inputs))
    return circuit

def boolean_circuit_weight(circuit):
    weight = 0
    for gate, inputs in circuit:
        if gate == 'AND':
            weight += sum(inputs)
        elif gate == 'OR':
            weight += len(inputs) - sum(inputs)
    return weight

def pearson_correlation(x, y):
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    denominator = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n))) * math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)))
    if denominator == 0:
        return 0
    return numerator / denominator

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_sizes = [5, 10, 15, 20, 30, 40]
    orders = []
    weights = []
    instances_tested = 0
    n_max = 0

    for size in n_sizes:
        for _ in range(5):  # Ensure at least 30 instances per seed
            circuit = generate_boolean_circuit(size)
            A = [[0] * size for _ in range(size)]
            for i, (gate, inputs) in enumerate(circuit):
                if gate == 'AND':
                    A[i][inputs[0]] += 1
                    A[i][inputs[1]] += 1
                elif gate == 'OR':
                    A[i][inputs[0]] += 1
                    A[i][inputs[1]] += 1
            order = min_eigenform_order(A)
            orders.append(order)
            weights.append(boolean_circuit_weight(circuit))
            instances_tested += 1
            n_max = max(n_max, size)

    correlation_coefficient = pearson_correlation(orders, weights)
    mean_absolute_deviation = sum(abs(o - w) for o, w in zip(orders, weights)) / len(orders)
    conjecture_holds = correlation_coefficient >= 0.8 and mean_absolute_deviation <= 3
    counterexample = "" if conjecture_holds else "correlation_coefficient=<{}> mean_abs_dev=<{}>".format(correlation_coefficient, mean_absolute_deviation)

    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL: {}".format(result))
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_value, std_value, support_fraction))
    elif support_fraction >= 0.8:
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_value, std_value, support_fraction))
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = results[first_failing_seed]["counterexample"]
        print("RESULT: FALSIFIED counterexample=\"{}\" first_failing_seed={}".format(counterexample, first_failing_seed))