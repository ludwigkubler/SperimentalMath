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
    
    def generate_boolean_circuit(depth, n):
        if depth == 0:
            return [random.choice([0, 1])]
        else:
            subcircuits = [generate_boolean_circuit(random.randint(0, depth-1), n) for _ in range(2)]
            return [subc[0] ^ subc[1] for subc in zip(subcircuits[0], subcircuits[1])]
    
    def gaussian_elimination(matrix):
        rows = len(matrix)
        cols = len(matrix[0])
        rank = 0
        pivot_col = 0
        
        for i in range(rows):
            if pivot_col >= cols:
                break
            
            max_row = i
            for j in range(i+1, rows):
                if abs(matrix[j][pivot_col]) > abs(matrix[max_row][pivot_col]):
                    max_row = j
            
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            if matrix[i][pivot_col] == 0:
                pivot_col += 1
                continue
            
            for j in range(rows):
                if j != i and matrix[j][pivot_col] != 0:
                    factor = -matrix[j][pivot_col] / matrix[i][pivot_col]
                    for k in range(cols):
                        matrix[j][k] += factor * matrix[i][k]
            
            pivot_col += 1
            rank += 1
        
        return rank
    
    def determinant(matrix):
        rows = len(matrix)
        cols = len(matrix[0])
        
        if rows != cols:
            raise ValueError("Matrix must be square")
        
        if rows == 1:
            return matrix[0][0]
        
        det = Fraction(0)
        sign = Fraction(1)
        for j in range(cols):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += sign * matrix[0][j] * determinant(submatrix)
            sign *= -Fraction(1)
        
        return det
    
    def tautological_ideal(circuit, n):
        variables = list(range(n))
        ideal = []
        for i in range(len(circuit)):
            if circuit[i]:
                monomial = [0] * n
                monomial[variables[i]] = 1
                ideal.append(monomial)
        return ideal
    
    def minimal_geometric_entropy(ideal):
        matrix = [[Fraction(x) for x in row] for row in ideal]
        rank = gaussian_elimination(matrix)
        return Fraction(rank, len(ideal))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            circuit = generate_boolean_circuit(random.randint(1, min(n-1, 5)), n)
            ideal = tautological_ideal(circuit, n)
            H_min = minimal_geometric_entropy(ideal)
            results.append((n, H_min))
    
    if not results:
        return {
            "metric_name": "minimal_geometric_entropy",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_min = min(n for _, _ in results)
    n_max = max(n for _, _ in results)
    H_min_values = [H_min for _, H_min in results]
    mean_H_min = sum(H_min_values) / len(H_min_values)
    std_H_min = math.sqrt(sum((x - mean_H_min) ** 2 for x in H_min_values) / len(H_min_values))
    
    if n_min < 5 or n_max < 20:
        return {
            "metric_name": "minimal_geometric_entropy",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "sub-asymptotic_n"
        }
    
    d_values = [n for n, _ in results]
    d_squared_log_n_values = [(d ** 2) * math.log(n) for d, n in results]
    mean_d_squared_log_n = sum(d_squared_log_n_values) / len(d_squared_log_n_values)
    std_d_squared_log_n = math.sqrt(sum((x - mean_d_squared_log_n) ** 2 for x in d_squared_log_n_values) / len(d_squared_log_n_values))
    
    correlation_coefficient = (sum((d_squared_log_n - mean_d_squared_log_n) * (H_min - mean_H_min) for d_squared_log_n, H_min in zip(d_squared_log_n_values, H_min_values)) /
                               (len(results) * std_d_squared_log_n * std_H_min))
    
    if correlation_coefficient < 0.9:
        return {
            "metric_name": "minimal_geometric_entropy",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": f"low_correlation_coefficient={correlation_coefficient:.2f}"
        }
    
    if all(abs(H_min - (d ** 2) * math.log(n)) / ((d ** 2) * math.log(n)) <= 0.1 for d, n, H_min in results):
        return {
            "metric_name": "minimal_geometric_entropy",
            "metric_value": mean_H_min,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        counterexample = f"instance with H_min={(d ** 2) * math.log(n)} not within ±10% of Θ(d^2 log n)"
        return {
            "metric_name": "minimal_geometric_entropy",
            "metric_value": mean_H_min,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": counterexample
        }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_H_min = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_H_min = math.sqrt(sum((result["metric_value"] - mean_H_min) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_H_min:.4f} std={std_H_min:.4f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_H_min:.4f} std={std_H_min:.4f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"low_correlation_coefficient\" first_failing_seed={first_failing_seed}")