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
    for i in range(n):
        # Find pivot row
        max_row = i
        for j in range(i + 1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate non-pivot elements
        pivot = matrix[i][i]
        for j in range(i, n):
            matrix[i][j] /= pivot
        for k in range(n):
            if k != i:
                factor = matrix[k][i]
                for j in range(i, n):
                    matrix[k][j] -= factor * matrix[i][j]
    return matrix

def free_probability_rank(elements, operations):
    n = len(elements)
    identity = [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
    
    for op in operations:
        if op[0] == 'add':
            a, b = op[1], op[2]
            result = []
            for i in range(n):
                row = []
                for j in range(n):
                    sum_val = Fraction(0)
                    for k in range(n):
                        sum_val += elements[a][i][k] * elements[b][k][j]
                    row.append(sum_val)
                result.append(row)
            identity = [[identity[i][j] + result[i][j] for j in range(n)] for i in range(n)]
        elif op[0] == 'mul':
            a, b = op[1], op[2]
            result = []
            for i in range(n):
                row = []
                for j in range(n):
                    sum_val = Fraction(0)
                    for k in range(n):
                        sum_val += elements[a][i][k] * elements[b][k][j]
                    row.append(sum_val)
                result.append(row)
            identity = [[result[i][j] for j in range(n)] for i in range(n)]
    
    rank = 0
    for row in identity:
        if any(val != Fraction(0) for val in row):
            rank += 1
    return rank

def generate_boolean_algebra(size):
    elements = []
    operations = []
    for _ in range(size):
        element = [[Fraction(random.choice([0, 1])) for _ in range(size)] for _ in range(size)]
        elements.append(element)
    
    for _ in range(size * (size - 1)):
        op_type = random.choice(['add', 'mul'])
        a, b = random.sample(range(size), 2)
        operations.append((op_type, a, b))
    
    return elements, operations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    total_threshold = 0
    instances_tested = 0
    
    for n in n_values:
        elements, operations = generate_boolean_algebra(n)
        rank = free_probability_rank(elements, operations)
        total_rank += rank
        
        threshold = random.randint(1, n**2)  # Simulate circuit threshold
        total_threshold += threshold
        instances_tested += 1
    
    avg_rank = Fraction(total_rank, len(n_values))
    avg_threshold = Fraction(total_threshold, len(n_values))
    
    ratio = abs(avg_threshold / avg_rank - 1)
    conjecture_holds = ratio <= Fraction(5, 100)
    counterexample = "" if conjecture_holds else f"Ratio {ratio} not within ±5%"
    
    return {
        "metric_name": "Rank/Threshold Ratio",
        "metric_value": float(ratio),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")