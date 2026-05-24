# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import product

# Helper functions for matrix operations and p-adic logarithm
def multiply_matrices(a, b):
    m = len(a)
    n = len(b[0])
    p = len(b)
    result = [[sum(a[i][k] * b[k][j] for k in range(p)) for j in range(n)] for i in range(m)]
    return result

def matrix_power(matrix, power):
    if power == 1:
        return matrix
    elif power % 2 == 0:
        half_power = matrix_power(matrix, power // 2)
        return multiply_matrices(half_power, half_power)
    else:
        return multiply_matrices(matrix, matrix_power(matrix, power - 1))

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        max_row = i
        for j in range(i + 1, rows):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        factor = Fraction(1, matrix[i][i])
        for j in range(cols):
            matrix[i][j] *= factor
        for j in range(rows):
            if i != j:
                factor = matrix[j][i]
                for k in range(cols):
                    matrix[j][k] -= factor * matrix[i][k]
    return matrix

def p_adic_log(x, p):
    if x <= 0:
        return float('inf')
    count = 0
    while x % p == 0:
        x //= p
        count += 1
    return -count

# Function to generate a random AC0 parity circuit of size s
def generate_ac0_circuit(s):
    n = int(math.log2(s)) + 1
    circuit = []
    for _ in range(s):
        gate = random.choice(['AND', 'OR'])
        inputs = random.sample(range(n), random.randint(1, n))
        circuit.append((gate, inputs))
    return circuit

# Function to compute the minimal non-Archimedean value of a boolean function
def compute_min_non_archimedean_value(circuit):
    n = len(circuit)
    p = 2
    max_val = float('inf')
    for _ in range(30):  # Sample 30 random inputs
        input_vector = [random.randint(0, 1) for _ in range(n)]
        value = 1
        for gate, inputs in circuit:
            if gate == 'AND':
                value *= input_vector[inputs[0]]
            else:  # OR
                value += input_vector[inputs[0]]
        max_val = min(max_val, abs(value))
    return p_adic_log(max_val, p)

# Function to run a single trial with a given seed
def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_ac0_circuit(n)
        min_non_archimedean_val = compute_min_non_archimedean_value(circuit)
        results.append(min_non_archimedean_val)
    
    mean_value = sum(results) / len(results)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in results) / len(results))
    
    return {
        "metric_name": "p-adic_log_min_non_archimedean",
        "metric_value": mean_value,
        "instances_tested": len(n_values),
        "conjecture_holds": std_value <= 0.7 * sum(n_values) / len(n_values),
        "counterexample": "" if std_value <= 0.7 * sum(n_values) / len(n_values) else "std_value > 0.7 * avg_n"
    }

# Main function to run multiple trials and print results
if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r['metric_value'] for r in results) / len(results)
    std_value = math.sqrt(sum((r['metric_value'] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r['counterexample'] != "" for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result['counterexample'] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")