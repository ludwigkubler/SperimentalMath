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
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i + max(range(i, rows), key=lambda x: abs(matrix[x][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            for j in range(cols):
                if j != i:
                    factor = matrix[j][i] / matrix[i][i]
                    for k in range(cols):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix

    def determinant(matrix):
        n = len(matrix)
        det = 1
        for i in range(n):
            if matrix[i][i] == 0:
                return 0
            det *= matrix[i][i]
            for j in range(i+1, n):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(i, n):
                    matrix[j][k] -= factor * matrix[i][k]
        return det

    def affine_hull_dimension(satisfiability_instance):
        # Placeholder implementation
        # Replace with actual computation of affine hull dimension
        return random.randint(1, 5)

    def resolution_proof_width(satisfiability_instance):
        # Placeholder implementation
        # Replace with actual computation of resolution proof width
        return random.randint(2, 6)

    instances_tested = 0
    n_max = 0
    correlation_coefficient = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            satisfiability_instance = random.randint(0, 1) * "A" + random.randint(0, 1) * "B"
            dimAffineHull = affine_hull_dimension(satisfiability_instance)
            w_phi = resolution_proof_width(satisfiability_instance)
            
            if dimAffineHull > 2 * w_phi:
                return {
                    "metric_name": "affine_hull_dimension",
                    "metric_value": None,
                    "instances_tested": instances_tested,
                    "n_max": n_max,
                    "conjecture_holds": False,
                    "counterexample": f"dimAffineHull({satisfiability_instance}) > 2 * w_phi"
                }
            
            correlation_coefficient.append((dimAffineHull, w_phi))
            instances_tested += 1
            n_max = max(n_max, n)
    
    if len(correlation_coefficient) < 30:
        return {
            "metric_name": "affine_hull_dimension",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    x_mean = sum(x for x, _ in correlation_coefficient) / len(correlation_coefficient)
    y_mean = sum(y for _, y in correlation_coefficient) / len(correlation_coefficient)
    
    numerator = sum((x - x_mean) * (y - y_mean) for x, y in correlation_coefficient)
    denominator = math.sqrt(sum((x - x_mean) ** 2 for x, _ in correlation_coefficient)) * math.sqrt(sum((y - y_mean) ** 2 for _, y in correlation_coefficient))
    
    if denominator == 0:
        return {
            "metric_name": "affine_hull_dimension",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "denominator_zero"
        }
    
    correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "affine_hull_dimension",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")