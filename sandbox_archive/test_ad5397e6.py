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
        for r in range(i+1, n):
            if abs(matrix[r][i]) > abs(matrix[max_row][i]):
                max_row = r
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below the pivot
        factor = Fraction(matrix[i][i])
        for j in range(i, n):
            matrix[i][j] /= factor
        
        for r in range(n):
            if r != i:
                factor = Fraction(matrix[r][i])
                for j in range(i, n):
                    matrix[r][j] -= factor * matrix[i][j]
    return matrix

def rank_variance(matrix):
    n = len(matrix)
    det = 1
    for i in range(n):
        if matrix[i][i] == 0:
            return None
        det *= matrix[i][i]
    return abs(det)

def cohomological_complex(graph, d):
    n = len(graph)
    complex_ = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if graph[i][j] == 1:
                complex_[i][j] = Fraction(d)
                complex_[j][i] = Fraction(d)
    return complex_

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            graph = [[0] * n for _ in range(n)]
            for i in range(n):
                neighbors = random.sample(range(n), d)
                for j in neighbors:
                    if i < j:
                        graph[i][j] = 1
                        graph[j][i] = 1
            
            complex_ = cohomological_complex(graph, d)
            beta2 = gaussian_elimination(complex_)
            rv = rank_variance(beta2)
            
            if rv is not None:
                results.append((beta2[0][0], rv))
    
    if len(results) < 30:
        return {
            "metric_name": "Rank Variance",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(len(result[0]) for result in results) if results else 0,
            "conjecture_holds": False,
            "counterexample": "Too few instances tested"
        }
    
    beta2_values = [result[0] for result in results]
    rv_values = [result[1] for result in results]
    
    mean_beta2 = sum(beta2_values) / len(beta2_values)
    mean_rv = sum(rv_values) / len(rv_values)
    std_rv = math.sqrt(sum((rv - mean_rv) ** 2 for rv in rv_values) / len(rv_values))
    
    support_fraction = sum(abs(b - r) <= 3 for b, r in zip(beta2_values, rv_values)) / len(results)
    
    return {
        "metric_name": "Rank Variance",
        "metric_value": mean_rv,
        "instances_tested": len(results),
        "n_max": max(len(result[0]) for result in results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else "support_fraction < 0.8"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
    
    results = [run_trial(seed) for seed in seeds]
    mean_rv = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_rv = math.sqrt(sum((result["metric_value"] - mean_rv) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rv} std={std_rv} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rv} std={std_rv} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"support_fraction < 0.8\" first_failing_seed={first_failing_seed}")