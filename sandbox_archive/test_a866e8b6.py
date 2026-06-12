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
    
    def generate_boolean_circuit(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_entanglement_complexity(circuit):
        # Simplified heuristic for entanglement complexity
        return sum(circuit.count(bit) for bit in set(circuit)) / len(circuit)
    
    def morse_function(circuit):
        n = int(math.log2(len(circuit)))
        return [sum(circuit[i:i+n]) % 2 for i in range(0, len(circuit), n)]
    
    def compute_minimal_geometric_defect(morse_func):
        critical_points = set()
        for i in range(len(morse_func)):
            if i == 0 or i == len(morse_func) - 1:
                continue
            if morse_func[i] != morse_func[i-1] and morse_func[i] != morse_func[i+1]:
                critical_points.add(i)
        return min(abs(cp1 - cp2) for cp1, cp2 in itertools.combinations(critical_points, 2))
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = Fraction(matrix[i][i])
            for j in range(i, n + 1):
                matrix[i][j] /= factor
            for j in range(n):
                if i != j:
                    factor = matrix[j][i]
                    for k in range(i, n + 1):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def matrix_multiply(A, B):
        m, n = len(A), len(B[0])
        result = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(len(B)):
                    result[i][j] += A[i][k] * B[k][j]
        return result
    
    def matrix_sub(A, B, mod):
        m, n = len(A), len(A[0])
        result = [[(A[i][j] - B[i][j]) % mod for j in range(n)] for i in range(m)]
        return result
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return abs(a * b) // gcd(a, b)
    
    def matrix_invert(matrix, mod):
        n = len(matrix)
        augmented_matrix = [row + [i == j for i in range(n)] for j, row in enumerate(matrix)]
        gaussian_elimination(augmented_matrix)
        identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        for i in range(n):
            matrix[i] = [augmented_matrix[i][j] for j in range(n)]
        return matrix
    
    def generate_random_matrix(m, n, mod):
        return [[random.randint(0, mod-1) for _ in range(n)] for _ in range(m)]
    
    def compute_mte(circuit):
        m = len(circuit)
        n = int(math.log2(m))
        A = generate_random_matrix(m, n, 2)
        B = generate_random_matrix(n, n, 2)
        C = matrix_multiply(A, B)
        D = matrix_sub(C, circuit, 2)
        E = matrix_invert(D, 2)
        return sum(sum(row) for row in E)
    
    def compute_metric(circuit):
        entanglement_complexity = compute_entanglement_complexity(circuit)
        morse_func = morse_function(circuit)
        minimal_geometric_defect = compute_minimal_geometric_defect(morse_func)
        mte = compute_mte(circuit)
        return {
            "metric_name": "minimal_geometric_defect",
            "metric_value": minimal_geometric_defect,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": minimal_geometric_defect <= entanglement_complexity * mte,
            "counterexample": ""
        }
    
    circuit = generate_boolean_circuit(5)
    metric = compute_metric(circuit)
    return metric

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i - 1 for i in range(2, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")