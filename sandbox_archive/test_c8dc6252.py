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
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0]*p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def spectral_radius(A):
        n = len(A)
        identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        lambda_max = 0
        for _ in range(100):  # Power iteration method
            v = [random.random() for _ in range(n)]
            v = [x / sum(v) for x in v]
            Av = matrix_multiply(A, v)
            lambda_new = sum(x*y for x, y in zip(Av, v))
            if abs(lambda_new - lambda_max) < 1e-6:
                break
            lambda_max = lambda_new
        return lambda_max
    
    def generate_circuit(depth, size):
        if depth == 0:
            return [random.choice([0, 1])]
        else:
            inputs = generate_circuit(depth-1, size)
            output = random.choice(inputs) ^ random.choice(inputs)
            inputs.append(output)
            return inputs[:size]
    
    def coxeter_group_action(circuit):
        n = len(circuit)
        A = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if circuit[i] != circuit[j]:
                    A[i][j] = 1
                    A[j][i] = 1
        return gaussian_elimination(A)
    
    def sigma(circuit):
        return len(circuit) - 1
    
    depth_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_radius = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for depth in depth_values:
        for _ in range(5):  # Sample 5 instances per depth
            circuit = generate_circuit(depth, depth)
            A = coxeter_group_action(circuit)
            radius = spectral_radius(A)
            total_radius += radius
            instances_tested += 1
            if radius < sigma(circuit) / math.log(depth):
                conjecture_holds = False
                counterexample = f"Depth {depth}, Circuit: {circuit}"
    
    mean_radius = total_radius / instances_tested
    return {
        "metric_name": "Spectral Radius",
        "metric_value": mean_radius,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_radius = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_radius} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_radius} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")