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
        for _ in range(n):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.choice('x' + ''.join(map(str, range(1, n+1)))) for _ in range(random.randint(2, 3))]
            circuit.append((gate_type, inputs))
        return circuit
    
    def evaluate_circuit(circuit, input_values):
        stack = []
        for gate_type, inputs in reversed(circuit):
            if gate_type == 'AND':
                result = True
                for inp in inputs:
                    if inp[0] == 'x':
                        result &= input_values[ord(inp[1:]) - ord('1')]
                    else:
                        result &= bool(int(inp))
                stack.append(result)
            elif gate_type == 'OR':
                result = False
                for inp in inputs:
                    if inp[0] == 'x':
                        result |= input_values[ord(inp[1:]) - ord('1')]
                    else:
                        result |= bool(int(inp))
                stack.append(result)
        return stack.pop()
    
    def tropical_rank(circuit):
        n = len(circuit)
        matrix = [[-math.inf for _ in range(n)] for _ in range(n)]
        for i, (gate_type, inputs) in enumerate(circuit):
            if gate_type == 'AND':
                for inp in inputs:
                    if inp[0] == 'x':
                        j = ord(inp[1:]) - ord('1')
                        matrix[i][j] = 0
                        matrix[j][i] = 0
            elif gate_type == 'OR':
                for inp in inputs:
                    if inp[0] == 'x':
                        j = ord(inp[1:]) - ord('1')
                        matrix[i][j] = 1
                        matrix[j][i] = 1
        
        def gaussian_elimination(A):
            m, n = len(A), len(A[0])
            for i in range(m):
                max_row = i
                for j in range(i+1, m):
                    if A[j][i] > A[max_row][i]:
                        max_row = j
                A[i], A[max_row] = A[max_row], A[i]
                for j in range(n):
                    A[i][j] /= A[i][i]
                for k in range(m):
                    if k != i:
                        factor = A[k][i]
                        for j in range(n):
                            A[k][j] -= factor * A[i][j]
            return A
        
        gaussian_elimination(matrix)
        
        rank = 0
        for row in matrix:
            if any(x > -math.inf for x in row):
                rank += 1
        return rank
    
    def generate_input_values(n):
        input_values = {}
        for i in range(1, n+1):
            input_values[f'x{i}'] = random.choice([0, 1])
        return input_values
    
    def compute_metric_value(circuit, input_values):
        result = evaluate_circuit(circuit, input_values)
        rank = tropical_rank(circuit)
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    for n in n_values:
        circuit = generate_circuit(n)
        input_values = generate_input_values(n)
        metric_value = compute_metric_value(circuit, input_values)
        metric_values.append(metric_value)
    
    mean_metric_value = sum(metric_values) / len(metric_values)
    std_metric_value = (sum((x - mean_metric_value) ** 2 for x in metric_values) / len(metric_values)) ** 0.5
    
    conjecture_holds = all(value >= math.log(n, 2) for n, value in zip(n_values, metric_values))
    
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "tropical_rank",
        "metric_value": mean_metric_value,
        "instances_tested": len(metric_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = (sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support")