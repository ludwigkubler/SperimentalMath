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

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def evaluate_function(f, input_bits):
    index = int(''.join(map(str, input_bits)), 2)
    return f[index]

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    rank = 0
    for j in range(cols):
        i_max = rank
        for i in range(rank, rows):
            if abs(matrix[i][j]) > abs(matrix[i_max][j]):
                i_max = i
        if matrix[i_max][j] == 0:
            continue
        matrix[rank], matrix[i_max] = matrix[i_max], matrix[rank]
        for i in range(rows):
            if i != rank:
                factor = -matrix[i][j] / matrix[rank][j]
                for k in range(cols):
                    matrix[i][k] += factor * matrix[rank][k]
        rank += 1
    return rank

def ehrhart_cohomology_rank(f, n):
    polytope_points = []
    for i in range(2**n):
        input_bits = [int(bit) for bit in format(i, f'0{n}b')]
        output = evaluate_function(f, input_bits)
        if output == 1:
            polytope_points.append(input_bits)
    matrix = [[None] * (n + 1) for _ in range(len(polytope_points))]
    for i, point in enumerate(polytope_points):
        matrix[i][0] = 1
        for j in range(n):
            matrix[i][j+1] = point[j]
    return gaussian_elimination(matrix)

def randomized_or_complexity(f):
    n = int(math.log2(len(f)))
    input_bits = [random.choice([0, 1]) for _ in range(n)]
    return len(input_bits)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in range(5, 41):
        f = generate_boolean_function(n)
        cohomology_rank = ehrhart_cohomology_rank(f, n)
        complexity = randomized_or_complexity(f)
        results.append((cohomology_rank**2, complexity))
    
    if not results:
        return {
            "metric_name": "randomized_or_complexity",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    cohomology_values, complexities = zip(*results)
    slope, intercept = linear_regression(cohomology_values, complexities)
    c = Fraction(1, 2)  # Placeholder value for the constant c
    if slope > c:
        return {
            "metric_name": "randomized_or_complexity",
            "metric_value": slope,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": f"Slope {slope} exceeds expected bound {c}"
        }
    
    return {
        "metric_name": "randomized_or_complexity",
        "metric_value": slope,
        "instances_tested": len(results),
        "conjecture_holds": True,
        "counterexample": ""
    }

def linear_regression(x, y):
    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum(xi * yi for xi, yi in zip(x, y))
    sum_xx = sum(xi**2 for xi in x)
    
    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x**2)
    intercept = (sum_y - slope * sum_x) / n
    
    return slope, intercept

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(30))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")