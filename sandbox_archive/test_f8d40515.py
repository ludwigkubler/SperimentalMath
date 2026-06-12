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
    rows, cols = len(matrix), len(matrix[0])
    for col in range(cols):
        max_row = col
        for row in range(col + 1, rows):
            if abs(matrix[row][col]) > abs(matrix[max_row][col]):
                max_row = row
        matrix[col], matrix[max_row] = matrix[max_row], matrix[col]
        factor = Fraction(-matrix[col][col], matrix[max_row][col])
        for r in range(cols):
            matrix[col][r] += factor * matrix[max_row][r]
    return matrix

def rank(matrix):
    rows, cols = len(matrix), len(matrix[0])
    row_echelon_form = gaussian_elimination(matrix)
    rank = 0
    for row in row_echelon_form:
        if any(row[i] != 0 for i in range(cols)):
            rank += 1
    return rank

def random_boolean_circuit(depth):
    n = depth * 2
    circuit = []
    for _ in range(n - 1):
        gate = random.choice(['AND', 'OR'])
        inputs = [random.randint(0, 1) for _ in range(gate.count('X'))]
        output = random.randint(0, 1)
        circuit.append((gate, inputs, output))
    return circuit

def tropical_representation(circuit):
    n = len(circuit)
    matrix = [[0] * (n + 1) for _ in range(n + 1)]
    for i, (gate, inputs, output) in enumerate(circuit):
        if gate == 'AND':
            for j in inputs:
                matrix[i][j] = 1
            matrix[i][n] = -output
        elif gate == 'OR':
            for j in inputs:
                matrix[j][i] = 1
            matrix[n][i] = output
    return matrix

def pearson_correlation(x, y):
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
    std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
    if std_x == 0 or std_y == 0:
        return 0
    return cov_xy / (std_x * std_y)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    depths = []
    ranks = []
    for _ in range(30):
        depth = random.randint(5, 40)
        circuit = random_boolean_circuit(depth)
        matrix = tropical_representation(circuit)
        rank_value = rank(matrix)
        depths.append(depth)
        ranks.append(rank_value)
    
    correlation_coefficient = pearson_correlation(depths, ranks)
    mean_rank = sum(ranks) / len(ranks)
    min_rank = min(ranks)
    conjecture_holds = correlation_coefficient >= 0.7 and min_rank >= mean_rank / 2
    counterexample = "" if conjecture_holds else "rank < half of average depth"
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(ranks),
        "n_max": max(depths),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_correlation = sum(r["metric_value"] for r in results) / len(results)
    std_deviation = math.sqrt(sum((r["metric_value"] - mean_correlation) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_correlation} std={std_deviation} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank < half of average depth\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")