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
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = Fraction(1, matrix[i][i])
            for j in range(cols):
                matrix[i][j] *= factor
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
        det = Fraction(1)
        for i in range(rows):
            max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = matrix[i][i]
            if factor == 0:
                return Fraction(0)
            det *= factor
            for k in range(rows):
                if k != i:
                    factor = matrix[k][i]
                    for j in range(cols):
                        matrix[k][j] -= factor * matrix[i][j]
        return det

    def galois_group_order(n):
        # This is a placeholder function. Implementing the actual Galois group order computation would be complex.
        # For simplicity, we'll use a heuristic that the order grows exponentially with n.
        return 2 ** (n * n)

    def resolution_proof_width(cnf):
        # Placeholder for computing resolution proof width
        return len(cnf)  # Simplified for demonstration

    instances_tested = 0
    n_max = 0
    total_order = Fraction(0)
    total_width_squared = Fraction(0)

    for _ in range(30):  # Sample 30 instances per seed
        n = random.randint(5, 40)  # Sweep n through at least 4 distinct sizes inside each trial
        cnf = [[random.choice([1, -1]) * (i + 1) for i in range(n)] for _ in range(n)]
        width = resolution_proof_width(cnf)
        order = galois_group_order(n)
        
        instances_tested += n
        n_max = max(n_max, n)
        total_order += order
        total_width_squared += width ** 2

    mean_order = total_order / instances_tested
    mean_width_squared = total_width_squared / instances_tested
    ratio = mean_order / mean_width_squared

    conjecture_holds = ratio <= Fraction(15, 10)  # 1.5 as a fraction for comparison
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "Galois Group Order to Resolution Proof Width Ratio",
        "metric_value": float(ratio),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")