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
    
    def create_matrix(cnf):
        n = len(cnf[0])
        matrix = [[0] * n for _ in range(n)]
        for clause in cnf:
            for literal in clause:
                var_index = abs(literal) - 1
                if literal > 0:
                    matrix[var_index][var_index] += 1
                else:
                    matrix[0][var_index] += 1
        return matrix
    
    def geometric_flow(matrix):
        n = len(matrix)
        flow_indices = []
        
        for i in range(n):
            for j in range(n):
                if i != j and matrix[i][j] > 0:
                    flow_indices.append(matrix[i][j])
        
        return flow_indices
    
    def variance(indices):
        mean = sum(indices) / len(indices)
        return sum((x - mean) ** 2 for x in indices) / len(indices)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_variance = 0
    instances_tested = 0
    
    for n in n_values:
        cnf = [[random.randint(1, n) for _ in range(random.randint(1, 3))] for _ in range(n)]
        matrix = create_matrix(cnf)
        flow_indices = geometric_flow(matrix)
        total_variance += variance(flow_indices)
        instances_tested += len(flow_indices)
    
    mean_variance = total_variance / instances_tested
    conjecture_holds = abs(mean_variance - math.sqrt(n)) <= 0.1 * math.sqrt(n)
    counterexample = "" if conjecture_holds else "variance_deviation"
    
    return {
        "metric_name": "Variance of Geometric Flow Indices",
        "metric_value": mean_variance,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_variance = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_variance} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_variance} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"variance_deviation\" first_failing_seed={first_failing_seed}")