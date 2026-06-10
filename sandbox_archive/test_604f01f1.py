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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        # Find the pivot row
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below the pivot
        for j in range(i+1, m):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_circuit(n):
        circuit = []
        for _ in range(2**n - 1):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(gate)]
            circuit.append((gate, inputs))
        return circuit
    
    def calculate_p_adic_metric(circuit):
        # Simplified p-adic metric calculation
        A = [[0] * (len(circuit) + 1) for _ in range(len(circuit) + 1)]
        for i in range(1, len(circuit) + 1):
            for j in range(i, len(circuit) + 1):
                if circuit[i-1][0] == 'AND':
                    A[i][j] = A[j][i] = abs(circuit[i-1][1].count(1) - circuit[j-1][1].count(1))
                elif circuit[i-1][0] == 'OR':
                    A[i][j] = A[j][i] = abs(len(circuit[i-1][1]) - len(circuit[j-1][1]))
        gaussian_elimination(A)
        rank = sum(1 for row in A if any(row))
        return rank
    
    def calculate_entanglement_complexity(circuit):
        # Simplified entanglement complexity calculation
        complexity = 0
        for gate, inputs in circuit:
            complexity += len(inputs)
        return complexity
    
    n_max = 40
    instances_tested = 30
    r_p_values = []
    e_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        circuit = generate_boolean_circuit(n)
        r_p = calculate_p_adic_metric(circuit)
        e = calculate_entanglement_complexity(circuit)
        r_p_values.append(r_p)
        e_values.append(e)
    
    if len(r_p_values) < 30:
        return {
            "metric_name": "r_p(C)",
            "metric_value": None,
            "instances_tested": len(r_p_values),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_r_p = sum(r_p_values) / len(r_p_values)
    mean_e = sum(e_values) / len(e_values)
    std_r_p = math.sqrt(sum((x - mean_r_p) ** 2 for x in r_p_values) / len(r_p_values))
    std_e = math.sqrt(sum((x - mean_e) ** 2 for x in e_values) / len(e_values))
    
    correlation_coefficient = sum((r_p_values[i] - mean_r_p) * (e_values[i] - mean_e) for i in range(len(r_p_values))) / (len(r_p_values) * std_r_p * std_e)
    mean_abs_diff = sum(abs(r_p_values[i] - e_values[i]) for i in range(len(r_p_values))) / len(r_p_values)
    
    conjecture_holds = correlation_coefficient >= 0.7 and mean_abs_diff <= 5
    
    return {
        "metric_name": "r_p(C)",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"correlation={correlation_coefficient}, mean_abs_diff={mean_abs_diff}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_r_p = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_r_p = math.sqrt(sum((r["metric_value"] - mean_r_p) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_r_p} std={std_r_p} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["metric_value"] is not None for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")