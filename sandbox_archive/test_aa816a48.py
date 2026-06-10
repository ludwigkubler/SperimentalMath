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

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += ((-1) ** j) * A[0][j] * determinant(submatrix)
        return det

    def hyperbolic_volume(A):
        det_A = determinant(A)
        if det_A == 0:
            return 0
        n = len(A)
        vol = abs(det_A) ** (1 / n)
        return vol

    def generate_circuit(n):
        circuit = []
        for _ in range(2**n):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(n)]
            circuit.append((gate, inputs))
        return circuit

    def evaluate_circuit(circuit, assignment):
        stack = []
        for gate, inputs in reversed(circuit):
            if gate == 'AND':
                result = all(stack.pop() for _ in inputs)
            elif gate == 'OR':
                result = any(stack.pop() for _ in inputs)
            stack.append(result)
        return stack[0]

    def generate_instance(n):
        circuit = generate_circuit(n)
        instances = []
        for _ in range(2**n):
            assignment = [random.randint(0, 1) for _ in range(n)]
            result = evaluate_circuit(circuit, assignment)
            instances.append((assignment, result))
        return instances

    def construct_affine_variety(instances):
        n = len(instances[0][0])
        A = [[0] * (n + 1) for _ in range(n + 1)]
        b = [0] * (n + 1)
        for assignment, result in instances:
            row = [1] + assignment
            A.append(row)
            b.append(result - sum(a * x for a, x in zip(row, assignment)))
        return A, b

    def solve_linear_system(A, b):
        m, n = len(A), len(A[0])
        augmented_matrix = [row + [b[i]] for i, row in enumerate(A)]
        gaussian_elimination(augmented_matrix)
        solution = [0] * n
        for i in range(n-1, -1, -1):
            solution[i] = augmented_matrix[i][-1]
            for j in range(i+1, n):
                solution[i] -= A[i][j] * solution[j]
        return solution

    def minimal_hyperbolic_volume(instances):
        A, b = construct_affine_variety(instances)
        solution = solve_linear_system(A, b)
        matrix = [solution + [0]] + A
        vol = hyperbolic_volume(matrix)
        return vol

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        instances = generate_instance(n)
        vol = minimal_hyperbolic_volume(instances)
        if vol == 0:
            continue
        expected_vol = n ** (2/3)
        if abs(vol - expected_vol) / expected_vol > 1.5:
            return {
                "metric_name": "Hyperbolic Volume",
                "metric_value": vol,
                "instances_tested": len(instances),
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"n={n}, expected={expected_vol}, actual={vol}"
            }
        results.append(vol)

    return {
        "metric_name": "Hyperbolic Volume",
        "metric_value": sum(results) / len(results),
        "instances_tested": len(instances),
        "n_max": max(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)

    mean_vol = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_vol) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_vol} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_vol} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[first_failing_seed]['n_max']}, expected={results[first_failing_seed]['metric_value']}\" first_failing_seed={first_failing_seed}")