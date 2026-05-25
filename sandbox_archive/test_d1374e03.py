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
        for j in range(n):
            if i != j:
                factor = Fraction(matrix[j][i], matrix[i][i])
                for k in range(n + 1):
                    matrix[j][k] -= factor * matrix[i][k]

    return matrix

def rank(matrix):
    n = len(matrix)
    rref_matrix = gaussian_elimination(matrix[:])
    rank = 0
    for row in rref_matrix:
        if any(row):
            rank += 1
    return rank

def configuration_space_metric(clauses):
    variables = set()
    for clause in clauses:
        variables.update(clause)
    
    n = len(variables)
    points = [[0] * n for _ in range(len(clauses))]
    distances = []
    
    var_index = {var: i for i, var in enumerate(sorted(variables))}
    
    for i, clause in enumerate(clauses):
        point = [0] * n
        for var in clause:
            if var.startswith('¬'):
                point[var_index[var[1:]]] = -1
            else:
                point[var_index[var]] = 1
        points[i] = point
    
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            dist = sum((points[i][k] - points[j][k]) ** 2 for k in range(n))
            distances.append(dist)
    
    return points, distances

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    variables = [f'x{i+1}' for i in range(n)]
    clauses = []
    for _ in range(2 * n):
        clause = random.sample(variables + ['¬' + var for var in variables], 3)
        if random.choice([True, False]):
            clause.append('¬' + random.choice(clauses))
        clauses.append(clause)
    
    points, distances = configuration_space_metric(clauses)
    rank_value = rank([[dist] for dist in distances])
    
    metric_name = "Minimal Rank"
    metric_value = rank_value
    instances_tested = len(distances)
    conjecture_holds = rank_value >= n**2 * math.log(n)
    counterexample = "" if conjecture_holds else f"Rank {rank_value} < {n**2 * math.log(n)}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")