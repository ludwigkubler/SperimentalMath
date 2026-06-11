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
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def noncommutative_polynomial_representation(circuit):
        n = int(math.log2(len(circuit)))
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n + 1):
            for j in range(n + 1):
                if i == j:
                    matrix[i][j] = 1
                elif i < j:
                    matrix[i][j] = circuit[i * (n + 1) + j]
                else:
                    matrix[i][j] = -circuit[j * (n + 1) + i]
        return matrix
    
    def entanglement_complexity(circuit):
        n = int(math.log2(len(circuit)))
        count = 0
        for i in range(n):
            for j in range(i + 1, n):
                if circuit[i * (n + 1) + j] != circuit[j * (n + 1) + i]:
                    count += 1
        return count
    
    def matrix_order(matrix):
        n = len(matrix)
        identity = [[0] * n for _ in range(n)]
        for i in range(n):
            identity[i][i] = 1
        
        def multiply(A, B):
            result = [[0] * n for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    for k in range(n):
                        result[i][j] += A[i][k] * B[k][j]
            return result
        
        def subtract(A, B):
            result = [[0] * n for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    result[i][j] = A[i][j] - B[i][j]
            return result
        
        def add(A, B):
            result = [[0] * n for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    result[i][j] = A[i][j] + B[i][j]
            return result
        
        def is_zero(matrix):
            for row in matrix:
                if any(x != 0 for x in row):
                    return False
            return True
        
        order = 1
        while True:
            new_matrix = multiply(matrix, identity)
            if is_zero(subtract(new_matrix, identity)):
                break
            matrix = add(matrix, new_matrix)
            order += 1
        return order
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_random_circuit(n)
        min_poly_rep_order = matrix_order(noncommutative_polynomial_representation(circuit))
        entanglement_complexity_val = entanglement_complexity(circuit)
        results.append((min_poly_rep_order, entanglement_complexity_val))
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n = len(results)
    x_sum, y_sum, xy_sum, x2_sum, y2_sum = 0, 0, 0, 0, 0
    
    for x, y in results:
        x_sum += x
        y_sum += y
        xy_sum += x * y
        x2_sum += x ** 2
        y2_sum += y ** 2
    
    mean_x = x_sum / n
    mean_y = y_sum / n
    numerator = n * xy_sum - x_sum * y_sum
    denominator = math.sqrt((n * x2_sum - x_sum ** 2) * (n * y2_sum - y_sum ** 2))
    
    if denominator == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": n,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "division_by_zero"
        }
    
    pearson_correlation = numerator / denominator
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_correlation,
        "instances_tested": n,
        "n_max": max(n_values),
        "conjecture_holds": pearson_correlation >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(r["metric_value"] is not None for r in results):
        mean_metric = sum(r["metric_value"] for r in results) / len(results)
        std_metric = math.sqrt(sum((r["metric_value"] - mean_metric) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed + 1}")
    else:
        print("RESULT: INCONCLUSIVE some_trials_failed")