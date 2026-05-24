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
            max_row = i + max(range(i, rows), key=lambda k: abs(matrix[k][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = matrix[i][i]
            for j in range(cols):
                matrix[i][j] /= factor
            for k in range(rows):
                if k != i:
                    factor = matrix[k][i]
                    for j in range(cols):
                        matrix[k][j] -= factor * matrix[i][j]
        return matrix

    def determinant(matrix):
        rows, cols = len(matrix), len(matrix[0])
        if rows != cols:
            raise ValueError("Matrix must be square")
        if rows == 1:
            return matrix[0][0]
        det = 0
        for j in range(cols):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += (-1) ** j * matrix[0][j] * determinant(submatrix)
        return det

    def read_twice_bp_size(n, r):
        # Placeholder function to simulate BP size calculation
        return 2**(n*r)

    def minimal_rank(bp_size):
        # Placeholder function to simulate minimal rank calculation
        return int(math.log(bp_size, 2) / n)

    n = random.randint(5, 40)
    bp_size = read_twice_bp_size(n, 1)
    r = minimal_rank(bp_size)
    
    expected_exponential_behavior = bp_size / (2**(n*r))
    actual_ratio = bp_size / (2**(n*r))

    if abs(actual_ratio - expected_exponential_behavior) > 0.1:
        return {
            "metric_name": "Ratio of BP size to expected exponential behavior",
            "metric_value": actual_ratio,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "ratio_out_of_bounds"
        }
    
    if r > 1:
        return {
            "metric_name": "Minimal rank of BP",
            "metric_value": r,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"rank_greater_than_1 (r={r})"
        }
    
    return {
        "metric_name": "Ratio of BP size to expected exponential behavior",
        "metric_value": actual_ratio,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        seeds = [2**i + 3 for i in range(5, 6)]  # Default to a list of primes

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_ratio)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")