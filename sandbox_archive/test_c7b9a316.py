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
    
    def generate_polynomial(n):
        return [random.randint(0, 1) for _ in range(n)]
    
    def evaluate_polynomial(poly, x):
        result = 0
        for i, coeff in enumerate(poly):
            result += coeff * (x ** i)
        return result
    
    def count_points_on_curve(polynomial, n):
        points = set()
        for x in range(2**n):
            y_squared = evaluate_polynomial(polynomial, x) % 2
            if y_squared == 0:
                points.add((x, 0))
                points.add((x, 1))
        return len(points)
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = 1 / matrix[i][i]
            for j in range(n):
                matrix[i][j] *= factor
            for j in range(n):
                if j != i:
                    factor = matrix[j][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def rank_of_matrix(matrix):
        n = len(matrix)
        augmented_matrix = [row + [1] for row in matrix]
        gaussian_elimination(augmented_matrix)
        rank = 0
        for i in range(n):
            if all(x == 0 for x in augmented_matrix[i]):
                continue
            rank += 1
        return rank
    
    def generate_explicit_function(n):
        return [random.randint(0, 1) for _ in range(n)]
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_points = 0
    num_instances = 30
    
    for n in n_values:
        for _ in range(num_instances):
            f = generate_explicit_function(n)
            s = len(f)
            points = count_points_on_curve(f, n)
            total_points += points
    
    mean_points = total_points / (len(n_values) * num_instances)
    
    conjecture_holds = mean_points >= 10 * math.log(30)  # Example threshold
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "mean_points",
        "metric_value": mean_points,
        "instances_tested": len(n_values) * num_instances,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_points = sum(r["metric_value"] for r in results) / len(results)
    std_points = math.sqrt(sum((r["metric_value"] - mean_points) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_points} std={std_points} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")