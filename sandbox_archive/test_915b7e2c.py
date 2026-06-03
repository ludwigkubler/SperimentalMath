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
    
    def generate_random_circuit(n):
        circuit = []
        for _ in range(2**n):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(n)]
            circuit.append((gate_type, inputs))
        return circuit
    
    def truth_table(circuit):
        n = len(circuit[0][1])
        table = {}
        for i in range(2**n):
            inputs = [(i >> j) & 1 for j in range(n)]
            output = evaluate_circuit(circuit, inputs)
            table[tuple(inputs)] = output
        return table
    
    def evaluate_circuit(circuit, inputs):
        stack = []
        for gate_type, inputs in circuit:
            if gate_type == 'AND':
                result = 1
                for input_val in inputs:
                    result &= input_val
                stack.append(result)
            elif gate_type == 'OR':
                result = 0
                for input_val in inputs:
                    result |= input_val
                stack.append(result)
        return stack[-1]
    
    def diophantine_degree(truth_table):
        n = int(math.log2(len(truth_table)))
        matrix = []
        for i in range(2**n):
            row = [truth_table[tuple(inputs)] for inputs in itertools.product([0, 1], repeat=n)]
            matrix.append(row)
        
        # Gaussian elimination to find the rank
        def gaussian_elimination(matrix):
            rows, cols = len(matrix), len(matrix[0])
            rank = 0
            for i in range(cols):
                if all(matrix[j][i] == 0 for j in range(rank, rows)):
                    continue
                matrix[rank], matrix[i] = matrix[i], matrix[rank]
                for j in range(rank + 1, rows):
                    factor = matrix[j][i] / matrix[rank][i]
                    for k in range(cols):
                        matrix[j][k] -= factor * matrix[rank][k]
                rank += 1
            return rank
        
        return gaussian_elimination(matrix)
    
    def monotone_width(circuit):
        n = len(circuit[0][1])
        max_width = 0
        for i in range(2**n):
            inputs = [(i >> j) & 1 for j in range(n)]
            width = sum(1 for gate_type, _ in circuit if any(input_val == 1 for input_val in gate_type))
            max_width = max(max_width, width)
        return max_width
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_random_circuit(n)
        truth_table_dict = truth_table(circuit)
        d_p = diophantine_degree(truth_table_dict)
        w_c = monotone_width(circuit)
        results.append((d_p, w_c))
    
    if len(results) < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_data"
        }
    
    d_ps = [d_p for d_p, _ in results]
    w_cs = [w_c for _, w_c in results]
    
    mean_d_p = sum(d_ps) / len(d_ps)
    mean_w_c = sum(w_cs) / len(w_cs)
    correlation = (sum((d_p - mean_d_p) * (w_c - mean_w_c) for d_p, w_c in results) /
                   math.sqrt(sum((d_p - mean_d_p)**2 for d_p in d_ps) *
                             sum((w_c - mean_w_c)**2 for w_c in w_cs)))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.7 and all(corr >= 0.6 for corr in [correlation]),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and any(result["metric_value"] < 0.6 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_below_threshold\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")