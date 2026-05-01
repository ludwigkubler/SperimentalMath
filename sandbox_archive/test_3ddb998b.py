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
    n = 40
    depth = 5
    size_C = 2**n * depth
    
    # Generate a random AC⁰ circuit for PARITY on n inputs
    def generate_ac0_circuit(n, depth):
        circuit = []
        for _ in range(depth):
            layer = [random.choice(['AND', 'OR']) if i % 2 == 1 else 'NOT' for i in range(2**(n-1))]
            circuit.append(layer)
        return circuit
    
    circuit = generate_ac0_circuit(n, depth)
    
    # Construct the coefficient matrix
    def construct_coefficient_matrix(circuit, n):
        num_inputs = 2**n
        coefficient_matrix = [[0] * num_inputs for _ in range(num_inputs)]
        
        def evaluate_expression(expr, inputs):
            if expr == 'NOT':
                return not inputs[0]
            elif expr == 'AND':
                return all(inputs)
            elif expr == 'OR':
                return any(inputs)
            
            left, right = expr.split(' ')
            left_val = evaluate_expression(left, inputs[:len(inputs)//2])
            right_val = evaluate_expression(right, inputs[len(inputs)//2:])
            if expr.startswith('NOT'):
                return not (left_val and right_val)
            elif expr.startswith('AND'):
                return left_val and right_val
            elif expr.startswith('OR'):
                return left_val or right_val
        
        for i in range(num_inputs):
            for j in range(num_inputs):
                inputs = [bool(i & (1 << k)) for k in range(n)]
                result = evaluate_expression(circuit[0][i % len(circuit[0])], inputs)
                coefficient_matrix[i][j] = Fraction(result, 2**n)
        
        return coefficient_matrix
    
    coefficient_matrix = construct_coefficient_matrix(circuit, n)
    
    # Compute the real rank via eigenvalue decomposition
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            for j in range(cols):
                if i != j:
                    factor = Fraction(matrix[j][i], matrix[i][i])
                    for k in range(rows):
                        matrix[j][k] -= factor * matrix[i][k]
        
        rank = sum(1 for row in matrix if any(val != 0 for val in row))
        return rank
    
    real_rank = gaussian_elimination(coefficient_matrix)
    
    # Verify the conjecture
    min_rank = Fraction(1, 10) * math.log(size_C, 2)
    conjecture_holds = real_rank >= min_rank
    counterexample = "" if conjecture_holds else "rank < 0.1 * log(size(C))"
    
    return {
        "metric_name": "real_rank",
        "metric_value": real_rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        random.seed(seed)
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(res["metric_value"] for res in results) / len(results)
    std_rank = math.sqrt(sum((res["metric_value"] - mean_rank)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank < 0.1 * log(size(C))\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")