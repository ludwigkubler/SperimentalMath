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

def gaussian_elimination(matrix):
    n = len(matrix)
    row_echelon_form = [row[:] for row in matrix]
    
    for col in range(n):
        max_row = next((i for i in range(col, n) if row_echelon_form[i][col] != 0), None)
        if max_row is None:
            continue
        
        # Swap rows
        row_echelon_form[col], row_echelon_form[max_row] = row_echelon_form[max_row], row_echelon_form[col]
        
        # Eliminate below the pivot
        for i in range(col + 1, n):
            factor = Fraction(-row_echelon_form[i][col], row_echelon_form[col][col])
            if factor == 0:
                continue
            for j in range(n):
                row_echelon_form[i][j] += factor * row_echelon_form[col][j]
    
    return row_echelon_form

def rank(matrix):
    n = len(matrix)
    row_echelon_form = gaussian_elimination(matrix)
    rank_value = sum(1 for row in row_echelon_form if any(row[i] != 0 for i in range(n)))
    return rank_value

def generate_random_circuit(depth, n=4):
    circuit = []
    for _ in range(depth):
        gate = random.choice(['AND', 'OR'])
        inputs = [random.randint(0, 1) for _ in range(n)]
        circuit.append((gate, inputs))
    return circuit

def tropical_matrix(circuit):
    n = len(circuit[0][1])
    matrix = [[0] * (n + 1) for _ in range(n + 1)]
    
    for gate, inputs in circuit:
        if gate == 'AND':
            for i in range(n):
                matrix[i][n] += inputs[i]
        elif gate == 'OR':
            for i in range(n):
                matrix[n][i] += inputs[i]
    
    return matrix

def run_trial(seed: int) -> dict:
    random.seed(seed)
    depths = [5, 10, 15, 20, 30, 40]
    metric_values = []
    instances_tested = 0
    n_max = 0
    
    for depth in depths:
        for _ in range(5):  # Generate 5 circuits per depth
            circuit = generate_random_circuit(depth)
            matrix = tropical_matrix(circuit)
            rank_value = rank(matrix)
            
            metric_values.append((depth, rank_value))
            instances_tested += 1
            n_max = max(n_max, len(circuit))
    
    if not metric_values:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "No circuits generated"
        }
    
    # Calculate Pearson correlation coefficient
    depths = [depth for depth, _ in metric_values]
    ranks = [rank_value for _, rank_value in metric_values]
    mean_depth = sum(depths) / len(depths)
    mean_rank = sum(ranks) / len(ranks)
    
    covariance = sum((d - mean_depth) * (r - mean_rank) for d, r in zip(depths, ranks))
    depth_variance = sum((d - mean_depth) ** 2 for d in depths)
    rank_variance = sum((r - mean_rank) ** 2 for r in ranks)
    
    if depth_variance == 0 or rank_variance == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Zero variance in depth or rank"
        }
    
    pearson_corr = covariance / (math.sqrt(depth_variance) * math.sqrt(rank_variance))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": pearson_corr >= 0.7 and all(rank_value >= depth / 2 for _, rank_value in metric_values),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results if res["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results if res["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds supported")