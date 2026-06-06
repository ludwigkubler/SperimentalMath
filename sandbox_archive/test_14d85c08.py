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
        if n == 1:
            return ['0']
        else:
            left = generate_circuit(n // 2)
            right = generate_circuit(n - n // 2)
            return [f'({l} OR {r})' for l in left] + [f'({l} AND {r})' for l in left] + [f'NOT {l}' for l in right]
    
    def evaluate_circuit(circuit, input_str):
        stack = []
        for token in circuit.split():
            if token == 'OR':
                b, a = stack.pop(), stack.pop()
                stack.append('1' if a == '1' or b == '1' else '0')
            elif token == 'AND':
                b, a = stack.pop(), stack.pop()
                stack.append('1' if a == '1' and b == '1' else '0')
            elif token == 'NOT':
                a = stack.pop()
                stack.append('1' if a == '0' else '0')
            else:
                stack.append(token)
        return stack[0]
    
    def threshold_function(circuit, n):
        inputs = [bin(x)[2:].zfill(n) for x in range(2**n)]
        outputs = [evaluate_circuit(circuit, input_str) for input_str in inputs]
        unique_outputs = set(outputs)
        return len(unique_outputs)
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(n):
            pivot_row = -1
            for j in range(rank, m):
                if matrix[j][i] == '1':
                    pivot_row = j
                    break
            if pivot_row != -1:
                matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
                for j in range(n):
                    if i != j and matrix[rank][j] == '1':
                        for k in range(n):
                            matrix[j][k] = (int(matrix[j][k]) + int(matrix[rank][k])) % 2
                rank += 1
        return rank
    
    def ramanujan_matrices(circuit, n):
        inputs = [bin(x)[2:].zfill(n) for x in range(2**n)]
        outputs = [evaluate_circuit(circuit, input_str) for input_str in inputs]
        matrix = [[int(outputs[j][i]) for i in range(n)] for j in range(2**n)]
        return gaussian_elimination(matrix)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        circuit = generate_circuit(n)
        num_matrices = ramanujan_matrices(circuit, n)
        log_n = math.log(n)
        results.append({
            "n": n,
            "num_matrices": num_matrices,
            "log_n": log_n
        })
    
    mean_num_matrices = sum(result["num_matrices"] for result in results) / len(results)
    std_num_matrices = math.sqrt(sum((result["num_matrices"] - mean_num_matrices) ** 2 for result in results) / len(results))
    correlation_coefficient = sum((result["num_matrices"] - mean_num_matrices) * (result["log_n"] - mean_log_n) for result in results) / (len(results) * std_num_matrices * std_log_n)
    
    return {
        "metric_name": "Ramanujan Matrices",
        "metric_value": mean_num_matrices,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": correlation_coefficient > 0.95,
        "counterexample": "" if correlation_coefficient > 0.95 else f"Correlation coefficient: {correlation_coefficient}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")