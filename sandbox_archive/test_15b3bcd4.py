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
    n = len(A)
    C = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def matrix_invert(A):
    n = len(A)
    I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    for k in range(n):
        pivot = A[k][k]
        if pivot == 0:
            raise ValueError("Matrix is not invertible")
        for j in range(n):
            A[k][j] /= pivot
            I[k][j] /= pivot
        for i in range(n):
            if i != k:
                factor = A[i][k]
                for j in range(n):
                    A[i][j] -= factor * A[k][j]
                    I[i][j] -= factor * I[k][j]
    return I

def gaussian_elimination(A, b):
    n = len(A)
    M = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(M[j][i]) > abs(M[max_row][i]):
                max_row = j
        M[i], M[max_row] = M[max_row], M[i]
        factor = M[i][i]
        for j in range(n):
            M[i][j] /= factor
        b[i] /= factor
        for j in range(i+1, n):
            factor = M[j][i]
            for k in range(n):
                M[j][k] -= factor * M[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = b[i]
        for j in range(i+1, n):
            x[i] -= M[i][j] * x[j]
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_circuit(n, D, G):
        # Generate a random circuit with depth D and gate count G
        gates = []
        for _ in range(G):
            if len(gates) == 0 or random.choice([True, False]):
                gates.append((random.randint(1, n), random.randint(1, n)))
            else:
                gates.append((random.randint(1, n),))
        return gates
    
    def compute_partition(circuit):
        # Compute the minimal number of integer partitions required
        partition = {}
        for gate in circuit:
            if len(gate) == 2:
                a, b = gate
                if a not in partition or b not in partition:
                    partition[a] = partition.get(a, 0) + 1
                    partition[b] = partition.get(b, 0) + 1
        return sum(partition.values())
    
    def compute_communication_complexity(circuit):
        # Compute the communication complexity rank of the circuit
        n = max(max(gate) for gate in circuit)
        A = [[0 for _ in range(n)] for _ in range(n)]
        b = [0] * n
        for gate in circuit:
            if len(gate) == 2:
                a, b = gate
                A[a-1][b-1] += 1
                A[b-1][a-1] += 1
                b[a-1] += 1
                b[b-1] += 1
        x = gaussian_elimination(A, b)
        return sum(x)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        for _ in range(5):
            circuit = generate_circuit(n, random.randint(1, n), random.randint(1, n))
            partition = compute_partition(circuit)
            communication_complexity = compute_communication_complexity(circuit)
            results.append({
                "n": n,
                "partition": partition,
                "communication_complexity": communication_complexity
            })
    
    if len(results) < 30:
        return {
            "metric_name": "Partition(C)",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    partition_values = [result["partition"] for result in results]
    communication_complexity_values = [result["communication_complexity"] for result in results]
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        denominator = math.sqrt(sum((x[i] - mean_x)**2 for i in range(n))) * math.sqrt(sum((y[i] - mean_y)**2 for i in range(n)))
        return numerator / denominator
    
    correlation = pearson_correlation(partition_values, communication_complexity_values)
    
    return {
        "metric_name": "Partition(C)",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": correlation > 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")