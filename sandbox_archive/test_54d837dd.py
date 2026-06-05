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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def convex_hull_lattice_points(f, n):
        # Simplified version of the convex hull algorithm
        points = [(i, f[i]) for i in range(2**n)]
        min_x = min(point[0] for point in points)
        max_x = max(point[0] for point in points)
        min_y = min(point[1] for point in points)
        max_y = max(point[1] for point in points)
        return (max_x - min_x + 1) * (max_y - min_y + 1)
    
    def matrix_rank(f, n):
        # Convert f to a matrix and compute its rank
        matrix = [[f[i ^ j] for j in range(n)] for i in range(2**n)]
        rank = 0
        for row in matrix:
            if any(row):
                rank += 1
                for other_row in matrix:
                    if other_row != row and all(other_row[j] == row[j] for j in range(n)):
                        other_row[:] = [0] * n
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_lattice_points = 0
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            f = generate_boolean_function(n)
            lattice_points = convex_hull_lattice_points(f, n)
            rank = matrix_rank(f, n)
            if lattice_points > 1.5 * rank:
                return {
                    "metric_name": "lattice_point_to_rank_ratio",
                    "metric_value": lattice_points / rank,
                    "instances_tested": instances_tested,
                    "n_max": n,
                    "conjecture_holds": False,
                    "counterexample": f"Function with {n} inputs has {lattice_points} lattice points and {rank} rank"
                }
            total_lattice_points += lattice_points
            total_rank += rank
            instances_tested += 1
    
    mean_ratio = total_lattice_points / (total_rank * len(n_values) * 5)
    return {
        "metric_name": "lattice_point_to_rank_ratio",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Function with {result['n_max']} inputs has {result['metric_value']} lattice points and {result['instances_tested']} rank\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")