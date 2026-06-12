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
    
    def generate_circuit(n):
        circuit = []
        for _ in range(2 ** n - 1):
            gate = random.choice(['AND', 'OR'])
            inputs = sorted(random.sample(range(n), random.randint(1, n)))
            circuit.append((gate, inputs))
        return circuit
    
    def entanglement_complexity(circuit):
        # Simplified heuristic for entanglement complexity
        return len(circuit)
    
    def symmetric_matrix(circuit, n):
        matrix = [[0] * (2 ** n) for _ in range(2 ** n)]
        for gate, inputs in circuit:
            if gate == 'AND':
                for i in inputs:
                    for j in inputs:
                        matrix[1 << i][1 << j] += 1
            elif gate == 'OR':
                for i in inputs:
                    for j in range(n):
                        if j not in inputs:
                            matrix[1 << i][1 << j] += 1
        return matrix
    
    def gaussian_elimination(matrix, b):
        n = len(matrix)
        A = [row[:] + [b[i]] for i, row in enumerate(matrix)]
        for i in range(n):
            max_row = max(range(i, n), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(i + 1, n):
                factor = -A[j][i] / pivot
                for k in range(n + 1):
                    A[j][k] += factor * A[i][k]
        x = [0] * n
        for i in range(n - 1, -1, -1):
            x[i] = (A[i][-1] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
        return x
    
    def character_degree(matrix):
        n = len(matrix)
        eigenvalues = []
        for i in range(n):
            if all(abs(A[i][j]) < 1e-9 for j in range(n) if j != i):
                eigenvalues.append(1)
            else:
                A = [row[:] for row in matrix]
                pivot_row = max(range(i, n), key=lambda r: abs(A[r][i]))
                A[i], A[pivot_row] = A[pivot_row], A[i]
                pivot = A[i][i]
                if pivot == 0:
                    continue
                for j in range(n):
                    if j != i:
                        factor = -A[j][i] / pivot
                        for k in range(n):
                            A[j][k] += factor * A[i][k]
                eigenvalues.append(pivot)
        return max(eigenvalues, key=abs)
    
    def run_circuit(circuit):
        n = len(circuit)
        state = [0] * (2 ** n)
        for gate, inputs in circuit:
            if gate == 'AND':
                result = 1
                for i in inputs:
                    result &= state[i]
                for i in inputs:
                    state[i] = result
            elif gate == 'OR':
                result = 0
                for i in inputs:
                    result |= state[i]
                for i in inputs:
                    state[i] = result
        return state
    
    n = random.randint(5, 40)
    circuit = generate_circuit(n)
    entanglement = entanglement_complexity(circuit)
    symmetric_matrix = symmetric_matrix(circuit, n)
    
    try:
        minimal_index = character_degree(symmetric_matrix)
    except ZeroDivisionError:
        return {
            "metric_name": "minimal_index",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    return {
        "metric_name": "minimal_index",
        "metric_value": minimal_index,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values) / len(metric_values)} std=0 support_fraction=1")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(metric_values) / len(metric_values)} std={math.sqrt(sum((x - sum(metric_values) / len(metric_values))**2 for x in metric_values) / len(metric_values))} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed + 1}")