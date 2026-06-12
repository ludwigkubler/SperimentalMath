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
    
    def gaussian_elimination(matrix, mod):
        n = len(matrix)
        for i in range(n):
            pivot = matrix[i][i]
            if pivot == 0:
                continue
            for j in range(i + 1, n):
                factor = (matrix[j][i] * pow(pivot, -1, mod)) % mod
                for k in range(i, n):
                    matrix[j][k] = (matrix[j][k] - factor * matrix[i][k]) % mod
        return matrix

    def matrix_mult(A, B, mod):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % mod
        return C

    def matrix_power(matrix, power, mod):
        n = len(matrix)
        result = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
        while power > 0:
            if power % 2 == 1:
                result = matrix_mult(result, matrix, mod)
            matrix = matrix_mult(matrix, matrix, mod)
            power //= 2
        return result

    def symplectic_invariant(circuit):
        n = len(circuit)
        identity = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
        invariant = identity
        for gate in circuit:
            if gate == 'H':
                H = [[1, 1], [1, -1]]
                invariant = matrix_mult(invariant, H, 2)
            elif gate == 'CNOT':
                CNOT = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]
                invariant = matrix_mult(invariant, CNOT, 2)
        return gaussian_elimination(invariant, 2)

    def entanglement_complexity(circuit):
        n = len(circuit)
        complexity = 0
        for gate in circuit:
            if gate == 'CNOT':
                complexity += 1
        return complexity

    n_max = 40
    instances_tested = 30
    metric_values = []
    conjecture_holds = True
    counterexample = ""

    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        circuit = [random.choice(['H', 'CNOT']) for _ in range(n)]
        order = symplectic_invariant(circuit)
        complexity = entanglement_complexity(circuit)
        
        if order == identity:
            continue
        
        metric_values.append(order[0][1] / (2 ** complexity))
    
    mean_value = sum(metric_values) / len(metric_values)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = len([v for v in metric_values if v <= n]) / len(metric_values)

    return {
        "metric_name": "Symplectic Invariant Order",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds supported")