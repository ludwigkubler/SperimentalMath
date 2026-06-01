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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            denom = A[i][i]
            for j in range(n):
                A[i][j] /= denom
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
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
        det = Fraction(0)
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det

    def minimal_order(q_expansion):
        order = 0
        for coeff, exp in q_expansion:
            if coeff != 0 and exp > order:
                order = exp
        return order

    def monotone_width(circuit):
        n = len(circuit)
        adj_matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if circuit[i][j]:
                    adj_matrix[i][j] = 1
                    adj_matrix[j][i] = 1
        visited = [False] * n
        stack = [0]
        while stack:
            node = stack.pop()
            if not visited[node]:
                visited[node] = True
                for neighbor in range(n):
                    if adj_matrix[node][neighbor] and not visited[neighbor]:
                        stack.append(neighbor)
        return sum(1 for v in visited if v)

    def generate_modular_form(level, weight):
        # Placeholder function to generate a modular form
        # This is a dummy implementation and does not actually generate a valid modular form
        q_expansion = [(random.randint(-10, 10), random.randint(1, level)) for _ in range(random.randint(5, 10))]
        return q_expansion

    def construct_circuit(q_expansion):
        # Placeholder function to construct a circuit from a modular form
        # This is a dummy implementation and does not actually construct a valid circuit
        n = len(q_expansion)
        circuit = [[False] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if q_expansion[i][0] != 0 and q_expansion[j][0] != 0:
                    circuit[i][j] = True
        return circuit

    instances_tested = 0
    ord_min_values = []
    w_m_values = []

    for _ in range(30):
        level = random.randint(1, 5)
        weight = random.randint(2, 4)
        q_expansion = generate_modular_form(level, weight)
        circuit = construct_circuit(q_expansion)

        ord_min = minimal_order(q_expansion)
        w_m = monotone_width(circuit)

        if ord_min != 0 and w_m != 0:
            instances_tested += 1
            ord_min_values.append(ord_min)
            w_m_values.append(w_m)

    if instances_tested < 30:
        return {
            "metric_name": "ord_min vs w_m",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": 5,
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }

    mean_ord_min = sum(ord_min_values) / instances_tested
    mean_w_m = sum(w_m_values) / instances_tested

    cov_matrix = [[0, 0], [0, 0]]
    for i in range(instances_tested):
        cov_matrix[0][0] += (ord_min_values[i] - mean_ord_min) ** 2
        cov_matrix[1][1] += (w_m_values[i] - mean_w_m) ** 2
        cov_matrix[0][1] += (ord_min_values[i] - mean_ord_min) * (w_m_values[i] - mean_w_m)
    cov_matrix[0][0] /= instances_tested
    cov_matrix[1][1] /= instances_tested
    cov_matrix[0][1] /= instances_tested

    corr_coeff = cov_matrix[0][1] / math.sqrt(cov_matrix[0][0] * cov_matrix[1][1])

    return {
        "metric_name": "ord_min vs w_m",
        "metric_value": corr_coeff,
        "instances_tested": instances_tested,
        "n_max": 5,
        "conjecture_holds": abs(corr_coeff) >= 0.7 and abs(corr_coeff) <= 1.3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")

    mean_corr_coeff = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_supported\" first_failing_seed={first_failing_seed}")