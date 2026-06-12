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
    
    def generate_circuit(n):
        circuit = []
        for _ in range(n):
            gate = random.choice(['AND', 'OR', 'NOT'])
            if gate == 'NOT':
                circuit.append((gate, random.randint(0, n-1)))
            else:
                inputs = random.sample(range(n), 2)
                circuit.append((gate, *inputs))
        return circuit
    
    def compute_entanglement_complexity(circuit):
        # Simplified entanglement complexity calculation
        return len(circuit) ** 0.5
    
    def construct_symmetric_matrix(circuit):
        n = len(circuit)
        matrix = [[0] * n for _ in range(n)]
        for gate, *inputs in circuit:
            if gate == 'NOT':
                matrix[inputs[0]][inputs[0]] += 1
            else:
                for i in inputs:
                    matrix[i][i] += 1
                    for j in inputs:
                        if i != j:
                            matrix[i][j] += 1
        return matrix
    
    def compute_minimal_index(matrix):
        n = len(matrix)
        char_degrees = [0] * n
        for i in range(n):
            char_degrees[i] = sum(matrix[i])
        return min(char_degrees)
    
    def gaussian_elimination(A, b):
        n = len(A)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            b[i] /= pivot
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
                    b[k] -= factor * b[i]
        return [b[i] for i in range(n)]
    
    def determinant(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [[A[i][k] for k in range(n) if k != j] for i in range(1, n)]
            det += ((-1) ** j) * A[0][j] * determinant(submatrix)
        return det
    
    def character_degree(matrix):
        n = len(matrix)
        identity_matrix = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        char_degrees = []
        for k in range(1, n + 1):
            eigenvalues = gaussian_elimination(matrix, [0] * (n - k) + [1])
            char_degree = sum(eigenvalue ** k for eigenvalue in eigenvalues)
            char_degrees.append(char_degree)
        return min(char_degrees)
    
    def run_circuit(circuit):
        n = len(circuit)
        state = [random.randint(0, 1) for _ in range(n)]
        for gate, *inputs in circuit:
            if gate == 'NOT':
                state[inputs[0]] = 1 - state[inputs[0]]
            elif gate == 'AND':
                state[inputs[0]] &= state[inputs[1]]
            else:
                state[inputs[0]] |= state[inputs[1]]
        return state
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        circuit = generate_circuit(n)
        entanglement_complexity = compute_entanglement_complexity(circuit)
        symmetric_matrix = construct_symmetric_matrix(circuit)
        minimal_index = character_degree(symmetric_matrix)
        
        metric_values.append(minimal_index / entanglement_complexity)
    
    mean_value = sum(metric_values) / len(metric_values)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values))
    conjecture_holds = abs(mean_value) > 0.1
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "minimal_index_over_entanglement_complexity",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")