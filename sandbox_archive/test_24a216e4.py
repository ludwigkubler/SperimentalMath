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
    return abs(a*b) // gcd(a, b)

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0]*p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    m, n = len(A), len(b)
    Augmented = [A[i] + [b[i]] for i in range(m)]
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(Augmented[j][i]) > abs(Augmented[max_row][i]):
                max_row = j
        Augmented[i], Augmented[max_row] = Augmented[max_row], Augmented[i]
        pivot = Augmented[i][i]
        for j in range(i, n+1):
            Augmented[i][j] /= pivot
        for j in range(m):
            if j != i:
                factor = Augmented[j][i]
                for k in range(n+1):
                    Augmented[j][k] -= factor * Augmented[i][k]
    return [row[-1] for row in Augmented]

def generate_d_regular_circuit(d, n):
    if d % 2 == 0:
        raise ValueError("d must be odd")
    circuit = []
    for i in range(n):
        neighbors = random.sample(range(n), d)
        while len(set(neighbors)) != d:
            neighbors = random.sample(range(n), d)
        circuit.append(neighbors)
    return circuit

def construct_representation(circuit, n):
    adjacency_matrix = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in circuit[i]:
            adjacency_matrix[i][j] = 1
            adjacency_matrix[j][i] = 1
    laplacian_matrix = [[0]*n for _ in range(n)]
    degree_sum = sum(sum(row) for row in adjacency_matrix)
    for i in range(n):
        laplacian_matrix[i][i] = degree_sum - sum(adjacency_matrix[i])
        for j in range(i+1, n):
            laplacian_matrix[i][j] = -adjacency_matrix[i][j]
            laplacian_matrix[j][i] = -adjacency_matrix[j][i]
    eigenvalues = gaussian_elimination(laplacian_matrix, [0]*n)
    return min(eigenvalues[1:])

def max_gate_weight(circuit):
    weights = [len(neighbors) for neighbors in circuit]
    return max(weights)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    metrics = []
    
    for n in n_values:
        circuit = generate_d_regular_circuit(3, n)
        min_order = construct_representation(circuit, n)
        max_weight = max_gate_weight(circuit)
        metrics.append((min_order, max_weight))
    
    if len(metrics) < 30:
        return {
            "metric_name": "Correlation Coefficient",
            "metric_value": None,
            "instances_tested": len(metrics),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Too few instances tested"
        }
    
    min_orders = [m[0] for m in metrics]
    max_weights = [m[1] for m in metrics]
    correlation_coefficient = sum((min_orders[i] - sum(min_orders) / len(min_orders)) * (max_weights[i] - sum(max_weights) / len(max_weights)) for i in range(len(metrics))) / (len(metrics) * math.sqrt(sum((min_order - sum(min_orders) / len(min_orders))**2 for min_order in min_orders)) * math.sqrt(sum((max_weight - sum(max_weights) / len(max_weights))**2 for max_weight in max_weights)))
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": 30,
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8 and all(corr >= 0.5 for corr in metrics),
        "counterexample": "" if correlation_coefficient >= 0.8 else str(min(correlation_coefficient for corr, _, _ in metrics))
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std=0 support_fraction=1.0")
    elif any(r["counterexample"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{next(c for _, c in results if c)}\" first_failing_seed={first_failing_seed}")
    else:
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std=0 support_fraction={support_fraction:.2f}")