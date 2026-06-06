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
    
    def generate_boolean_circuit(n):
        circuit = []
        for _ in range(2**n):
            gate = random.choice(['AND', 'OR'])
            inputs = random.sample(range(n), 2)
            circuit.append((gate, inputs))
        return circuit
    
    def evaluate_circuit(circuit, input_values):
        stack = list(input_values)
        for gate, inputs in circuit:
            a, b = stack.pop(), stack.pop()
            if gate == 'AND':
                stack.append(a and b)
            else:
                stack.append(a or b)
        return stack[0]
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            # Find pivot
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            # Swap rows
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            # Eliminate below pivot
            for j in range(i+1, n):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def is_ramanujan_matrix(matrix):
        # Check if the matrix is non-singular
        det = 1.0
        n = len(matrix)
        for i in range(n):
            det *= matrix[i][i]
        return det != 0
    
    def threshold_function(circuit, input_values):
        return evaluate_circuit(circuit, input_values) >= 0.5
    
    def count_ramanujan_matrices(circuit):
        n = len(circuit)
        max_n = 2**n
        matrix_size = n * (n + 1)
        matrices = []
        
        for i in range(max_n):
            indicator = [bool(i & (1 << j)) for j in range(n)]
            if threshold_function(circuit, indicator):
                matrices.append(indicator)
        
        count = 0
        while len(matrices) > 0:
            matrix = matrices.pop()
            if is_ramanujan_matrix(matrix):
                count += 1
                for i in range(len(matrices)):
                    if all(matrix[j] == matrices[i][j] for j in range(n)):
                        matrices.pop(i)
                        break
        
        return count
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_boolean_circuit(n)
        instances_tested = 2**n
        total_ramanujan_matrices = sum(count_ramanujan_matrices(circuit) for _ in range(instances_tested))
        metric_value = total_ramanujan_matrices / instances_tested
        n_max = n
        conjecture_holds = True
        counterexample = ""
        
        if len(results) > 0:
            log_n_values = [math.log(n_val) for n_val in n_values]
            correlation_coefficient = sum((results[i] - metric_value) * (log_n_values[i] - math.log(sum(log_n_values))) for i in range(len(n_values))) / len(n_values)
            if abs(correlation_coefficient) < 0.05:
                conjecture_holds = False
                counterexample = "correlation_coefficient_too_low"
        
        results.append(metric_value)
    
    mean_metric_value = sum(results) / len(results)
    std_metric_value = math.sqrt(sum((x - mean_metric_value)**2 for x in results) / len(results))
    support_fraction = sum(1 for result in results if result <= 0.5 * math.log(n_values[-1])) / len(results)
    
    return {
        "metric_name": "#RamanujanMatrices",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested * len(n_values),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean_metric_value = sum(results) / len(results)
    std_metric_value = math.sqrt(sum((x - mean_metric_value)**2 for x in results) / len(results))
    support_fraction = sum(1 for result in results if result <= 0.5 * math.log(seeds[-1])) / len(results)
    
    if all(result <= 0.5 * math.log(seeds[-1]) for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(result > 0.5 * math.log(seeds[-1]) for result in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_too_low\" first_failing_seed={seeds[results.index(max(results))]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(seeds)}")