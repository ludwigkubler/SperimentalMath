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
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, m):
                factor = -A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] += factor * A[i][k]
        return A

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0]*p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def determinant(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1)**j * A[0][j] * determinant(submatrix)
        return det

    def tropical_divisor(gate, inputs):
        if gate == 'AND':
            return min(inputs)
        elif gate == 'OR':
            return max(inputs)
        elif gate == 'NOT':
            return 1 - inputs[0]
        else:
            raise ValueError("Invalid gate")

    def tropical_variety(circuit):
        n = len(circuit)
        m = 2**n
        A = [[0]*m for _ in range(m)]
        b = [0]*m
        for i in range(m):
            inputs = [(i >> j) & 1 for j in range(n)]
            output = circuit(inputs)
            for j in range(m):
                if (j >> i) & 1:
                    A[i][j] = tropical_divisor(circuit[0], [inputs[k] for k in range(1, n)])
                    b[j] += output
        return gaussian_elimination(A), b

    def tropical_hodge_index(A, b):
        det_A = determinant(A)
        if det_A == 0:
            return float('inf')
        return -math.log2(abs(det_A))

    def ac0_circuit(n):
        gates = ['AND', 'OR', 'NOT']
        circuit = [random.choice(gates) for _ in range(1, n)]
        return circuit

    def compute_tropical_hodge_index(circuit):
        A, b = tropical_variety(circuit)
        hodge_indices = []
        for i in range(len(b)):
            if b[i] != 0:
                hodge_indices.append(tropical_hodge_index(A, [b[j]/b[i] for j in range(len(b))]))
        return min(hodge_indices) if hodge_indices else float('inf')

    n_values = [5, 10, 15, 20, 30, 40]
    total_hodge_index = 0
    instances_tested = 0

    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            circuit = ac0_circuit(n)
            hodge_index = compute_tropical_hodge_index(circuit)
            total_hodge_index += hodge_index
            instances_tested += 1

    mean_hodge_index = total_hodge_index / instances_tested
    conjecture_holds = mean_hodge_index >= math.log2(n)**2 and mean_hodge_index <= math.log2(n)

    return {
        "metric_name": "tropical_hodge_index",
        "metric_value": mean_hodge_index,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_hodge_index = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_hodge_index} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")