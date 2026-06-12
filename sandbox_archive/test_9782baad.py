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
            for j in range(i + 1, m):
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

    def tropical_add(x, y):
        if x == float('-inf') or y == float('-inf'):
            return max(x, y)
        return x + y

    def tropical_multiply(x, y):
        if x == float('-inf') or y == float('-inf'):
            return float('-inf')
        return min(x, y)

    def tropical_rank(A):
        A_tropical = [[tropical_add(a[i][j], a[j][i]) for j in range(len(a))] for i in range(len(a))]
        rank = 0
        for row in gaussian_elimination(A_tropical):
            if any(row):
                rank += 1
        return rank

    def random_boolean_circuit(n, depth):
        if depth == 0:
            return [[random.choice([True, False])]]
        else:
            inputs = [random_boolean_circuit(n, depth - 1) for _ in range(2)]
            gates = ['AND', 'OR', 'XOR']
            gate = random.choice(gates)
            output = []
            if gate == 'AND':
                output = [[tropical_multiply(x[0], y[0]) for x, y in zip(i, j)] for i, j in zip(inputs[0], inputs[1])]
            elif gate == 'OR':
                output = [[tropical_add(x[0], y[0]) for x, y in zip(i, j)] for i, j in zip(inputs[0], inputs[1])]
            else:
                output = [[tropical_multiply(tropical_add(x[0], y[0]), tropical_add(not x[0], not y[0])) for x, y in zip(i, j)] for i, j in zip(inputs[0], inputs[1])]
            return output

    def entanglement_complexity(circuit):
        n = len(circuit)
        if n == 1:
            return 0
        else:
            return 1 + max(entanglement_complexity(subcircuit) for subcircuit in circuit)

    n_max = 40
    instances_tested = 30
    mtr_values = []
    ec_values = []

    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        circuit = random_boolean_circuit(n, depth=2)
        mtr_value = tropical_rank(circuit)
        ec_value = entanglement_complexity(circuit)
        mtr_values.append(mtr_value)
        ec_values.append(ec_value)

    correlation_coefficient = sum((mtr_values[i] - mean_mtr) * (ec_values[i] - mean_ec) for i in range(instances_tested)) / instances_tested
    mean_mtr = sum(mtr_values) / instances_tested
    mean_ec = sum(ec_values) / instances_tested

    conjecture_holds = abs(correlation_coefficient) >= 0.8 and all(abs(mtr - ec) <= 3 for mtr, ec in zip(mtr_values, ec_values))
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")