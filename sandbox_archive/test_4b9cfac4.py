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
    
    def generate_boolean_circuit(size):
        circuit = []
        for _ in range(size):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(2, 4))]
            circuit.append((gate_type, inputs))
        return circuit
    
    def compute_associated_matrix(circuit):
        n = len(circuit)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for i, (gate_type, inputs) in enumerate(circuit):
            if gate_type == 'AND':
                A[i][i] = -1
                for j in inputs:
                    A[j][i] = 1
            elif gate_type == 'OR':
                A[i][i] = -1
                for j in inputs:
                    A[j][i] = 1
        return A
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for k in range(i + 1, n):
                if abs(A[k][i]) > abs(A[max_row][i]):
                    max_row = k
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            for j in range(i + 1, n):
                factor = A[j][i] / A[i][i]
                for k in range(n + 1):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def minimal_order(A):
        A = gaussian_elimination(A)
        rank = sum(1 for row in A if any(row))
        return rank
    
    def circuit_weight(circuit):
        weight = 0
        for gate_type, inputs in circuit:
            weight += len(inputs) + 1
        return weight
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    max_n = 0
    correlation_coefficient = None
    counterexample = ""
    
    for n in n_values:
        if n > max_n:
            max_n = n
        for _ in range(5):  # Ensure at least 30 instances per seed
            circuit = generate_boolean_circuit(n)
            A = compute_associated_matrix(circuit)
            order = minimal_order(A)
            weight = circuit_weight(circuit)
            total_metric_value += order
            instances_tested += 1
    
    mean_metric_value = total_metric_value / instances_tested
    if instances_tested < 30:
        return {
            "metric_name": "MinimalOrder",
            "metric_value": mean_metric_value,
            "instances_tested": instances_tested,
            "n_max": max_n,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    # Calculate Pearson correlation coefficient
    x = [circuit_weight(generate_boolean_circuit(n)) for n in n_values for _ in range(5)]
    y = [minimal_order(compute_associated_matrix(generate_boolean_circuit(n))) for n in n_values for _ in range(5)]
    if len(x) != len(y):
        return {
            "metric_name": "MinimalOrder",
            "metric_value": mean_metric_value,
            "instances_tested": instances_tested,
            "n_max": max_n,
            "conjecture_holds": False,
            "counterexample": "mismatched_data"
        }
    
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    denominator = math.sqrt(sum((xi - mean_x) ** 2 for xi in x)) * math.sqrt(sum((yi - mean_y) ** 2 for yi in y))
    if denominator == 0:
        return {
            "metric_name": "MinimalOrder",
            "metric_value": mean_metric_value,
            "instances_tested": instances_tested,
            "n_max": max_n,
            "conjecture_holds": False,
            "counterexample": "division_by_zero"
        }
    correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "MinimalOrder",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": correlation_coefficient >= 0.8 and abs(mean_metric_value - sum(y) / n) <= 3,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")