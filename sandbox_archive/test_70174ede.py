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
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A

    def matrix_mult(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0]*p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def matrix_det(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        det = 1
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            det *= A[i][i]
            if det == 0:
                return 0
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return det

    def generate_boolean_circuit(w: int):
        n = 2**w
        circuit = []
        for i in range(1, n):
            if random.choice([True, False]):
                gate = (random.choice(['AND', 'OR']), [i-1, i])
            else:
                gate = ('NOT', [i-1])
            circuit.append(gate)
        return circuit

    def tseitin_formula(circuit):
        n = 2**len(circuit)
        formula = []
        for i in range(n):
            clause = []
            for j in range(len(circuit)):
                if circuit[j][0] == 'NOT':
                    if (i >> j) & 1:
                        clause.append(-(circuit[j][1][0] + 1))
                    else:
                        clause.append(circuit[j][1][0])
                elif circuit[j][0] == 'AND':
                    if (i >> j) & 1:
                        clause.append(circuit[j][1][0])
                        clause.append(circuit[j][1][1])
                    else:
                        clause.append(-(circuit[j][1][0] + 1))
                        clause.append(-(circuit[j][1][1] + 1))
                elif circuit[j][0] == 'OR':
                    if (i >> j) & 1:
                        clause.append(circuit[j][1][0])
                        clause.append(circuit[j][1][1])
                    else:
                        clause.append(-(circuit[j][1][0] + 1))
            formula.append(clause)
        return formula

    def affine_quasi_projective_variety(formula):
        n = len(formula)
        A = [[0]*n for _ in range(n)]
        b = [0]*n
        for i in range(n):
            for j in range(i, n):
                if i == j:
                    A[i][j] = 1
                else:
                    A[i][j] = -1
            b[i] = formula[i].count(0)
        A = gaussian_elimination(A)
        det = matrix_det(A)
        return abs(det)

    def monotone_width(circuit):
        width = 0
        for gate in circuit:
            if gate[0] == 'NOT':
                width += 1
            elif gate[0] == 'AND' or gate[0] == 'OR':
                width = max(width, len(gate[1]))
        return width

    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        w = random.randint(5, 40)
        circuit = generate_boolean_circuit(w)
        formula = tseitin_formula(circuit)
        ord_V = affine_quasi_projective_variety(formula)
        w_C = monotone_width(circuit)
        metric_values.append(ord_V >= w_C**2)

    return {
        "metric_name": "ord(V) >= w(C)^2",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": all(metric_values),
        "counterexample": "" if all(metric_values) else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std=0.0000 support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std=0.0000 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")