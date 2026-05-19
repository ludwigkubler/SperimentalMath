# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import defaultdict

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def log2(x):
        return math.log2(x)

    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = max(range(i, n), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            factor = 1 / A[i][i]
            for j in range(n):
                A[i][j] *= factor
            b[i] *= factor
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
                    b[k] -= factor * b[i]
        return [b[i] / A[i][i] for i in range(n)]

    def matrix_mult(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def matrix_power(M, k):
        n = len(M)
        result = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
        while k > 0:
            if k % 2 == 1:
                result = matrix_mult(result, M)
            M = matrix_mult(M, M)
            k //= 2
        return result

    def trace(A):
        n = len(A)
        return sum(A[i][i] for i in range(n))

    def det(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        elif n == 2:
            return A[0][0] * A[1][1] - A[0][1] * A[1][0]
        else:
            det_val = 0
            for j in range(n):
                submatrix = [row[:j] + row[j+1:] for row in A[1:]]
                det_val += (-1) ** j * A[0][j] * det(submatrix)
            return det_val

    def inv(A):
        n = len(A)
        det_A = det(A)
        if det_A == 0:
            raise ValueError("Matrix is singular")
        adjoint = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                submatrix = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
                cofactor = det(submatrix)
                adjoint[j][i] = (-1) ** (i+j) * cofactor
        return matrix_mult(adjoint, 1 / det_A)

    def random_matrix(n):
        return [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]

    def random_vector(n):
        return [random.randint(0, 1) for _ in range(n)]

    def evaluate_circuit(circuit, inputs):
        n = len(inputs)
        stack = []
        for gate in circuit:
            if isinstance(gate, int):  # Input literal
                stack.append(inputs[gate])
            else:  # Gate operation
                b = stack.pop()
                a = stack.pop()
                if gate == 'AND':
                    stack.append(a and b)
                elif gate == 'OR':
                    stack.append(a or b)
                elif gate == 'NOT':
                    stack.append(not a)
        return stack[0]

    def estimate_p_g(circuit, n):
        N = min(2**n, 16384)
        count = sum(evaluate_circuit(circuit, [random.randint(0, 1) for _ in range(n)]) for _ in range(N))
        return count / N

    def psi(C):
        m = len(C)
        total_log_bias = 0
        for g in C:
            p_g = estimate_p_g(g, n)
            min_p_g = min(p_g, 1 - p_g)
            max_min_p_g = max(min_p_g, 1 / (2 * m))
            total_log_bias += -log2(2 * max_min_p_g)
        return total_log_bias / m

    def generate_hastad_circuit(n, d):
        if d == 2:
            return [[i] for i in range(n)] + [['AND', i, j] for i in range(n) for j in range(i+1, n)]
        elif d == 3:
            blocks = [generate_hastad_circuit(int(math.sqrt(n)), d-1) for _ in range(int(math.sqrt(n)))]
            return [[i] for i in range(n)] + [['OR', block[0], block[1]] for block in blocks]
        elif d == 4:
            blocks = [generate_hastad_circuit(int(math.pow(n, 0.25)), d-1) for _ in range(int(math.pow(n, 0.25)))]
            return [[i] for i in range(n)] + [['OR', block[0], block[1]] for block in blocks]

    def generate_random_circuit(n, m):
        gates = []
        inputs = list(range(n))
        for _ in range(m):
            gate_type = random.choice(['AND', 'OR'])
            if gate_type == 'NOT':
                inputs.append(['NOT', random.choice(inputs)])
            else:
                inputs.append([gate_type, random.choice(inputs), random.choice(inputs)])
        return inputs

    def generate_or_circuit(n):
        return [[i] for i in range(n)] + [['OR'] * (n-1)]

    n_values = [6, 8, 10, 12, 16, 20, 24, 30]
    d_values = [2, 3, 4]
    results = []

    for n in n_values:
        for d in d_values:
            # Håstad-style AC⁰ PARITY circuits
            circuit_type = 'PARITY'
            if circuit_type == 'PARITY':
                circuit = generate_hastad_circuit(n, d)
                psi_value = psi(circuit)
                results.append({
                    "metric_name": "psi",
                    "metric_value": psi_value,
                    "instances_tested": 1,
                    "conjecture_holds": psi_value <= log2(len(circuit)) + 1,
                    "counterexample": "" if psi_value <= log2(len(circuit)) + 1 else f"psi({n},{d})={psi_value} > {log2(len(circuit)) + 1}"
                })

            # AC⁰ circuits of matching size computing random non-PARITY functions
            circuit_type = 'RANDOM'
            if circuit_type == 'RANDOM':
                circuit = generate_random_circuit(n, len(generate_hastad_circuit(n, d)))
                psi_value = psi(circuit)
                results.append({
                    "metric_name": "psi",
                    "metric_value": psi_value,
                    "instances_tested": 1,
                    "conjecture_holds": psi_value <= log2(len(circuit)) + 1,
                    "counterexample": "" if psi_value <= log2(len(circuit)) + 1 else f"psi({n},{d})={psi_value} > {log2(len(circuit)) + 1}"
                })

            # Tiny AC⁰ computing the OR_n function
            circuit_type = 'OR'
            if circuit_type == 'OR':
                circuit = generate_or_circuit(n)
                psi_value = psi(circuit)
                results.append({
                    "metric_name": "psi",
                    "metric_value": psi_value,
                    "instances_tested": 1,
                    "conjecture_holds": psi_value <= log2(len(circuit)) + 1,
                    "counterexample": "" if psi_value <= log2(len(circuit)) + 1 else f"psi({n},{d})={psi_value} > {log2(len(circuit)) + 1}"
                })

    return {
        "metric_name": "psi",
        "metric_value": sum(trial["metric_value"] for trial in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": all(trial["conjecture_holds"] for trial in results),
        "counterexample": "" if all(trial["conjecture_holds"] for trial in results) else f"psi({n},{d})={trial['metric_value']} > {log2(len(circuit)) + 1}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)

    mean_psi = sum(trial["metric_value"] for trial in results) / len(results)
    support_fraction = sum(trial["conjecture_holds"] for trial in results) / len(results)
    
    if all(trial["conjecture_holds"] for trial in results):
        print(f"RESULT: SUPPORTED mean={mean_psi} std=0.0 support_fraction={support_fraction}")
    elif any(not trial["conjecture_holds"] for trial in results):
        first_failing_seed = next(seed for seed, trial in zip(seeds, results) if not trial["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"psi({n},{d})={trial['metric_value']} > {log2(len(circuit)) + 1}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")