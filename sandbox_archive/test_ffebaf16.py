# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
import math
import itertools

def generate_random_boolean_function(n: int) -> list:
    return [random.choice([0, 1]) for _ in range(2**n)]

def compute_diophantine_equation_complexity(f: list) -> int:
    n = int(math.log2(len(f)))
    if 2**n != len(f):
        raise ValueError("Input list length must be a power of 2")
    
    matrix = [[Fraction(f[i * (1 << j)], 1) if i & (1 << j) else Fraction(0, 1) for j in range(n)] for i in range(1 << n)]
    rank = gaussian_elimination(matrix)
    return rank

def gaussian_elimination(matrix: list) -> int:
    rows, cols = len(matrix), len(matrix[0])
    pivot_row = 0
    pivot_col = 0
    
    while pivot_row < rows and pivot_col < cols:
        # Find the pivot element in the current column
        pivot = None
        for i in range(pivot_row, rows):
            if matrix[i][pivot_col] != Fraction(0, 1):
                pivot = i
                break
        
        if pivot is None:
            pivot_col += 1
            continue
        
        # Swap the pivot row with the current row
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        
        # Eliminate all other elements in the current column
        for i in range(rows):
            if i != pivot_row:
                factor = -matrix[i][pivot_col] / matrix[pivot_row][pivot_col]
                for j in range(cols):
                    matrix[i][j] += factor * matrix[pivot_row][j]
        
        pivot_row += 1
        pivot_col += 1
    
    return sum(1 for row in matrix if any(x != Fraction(0, 1) for x in row))

def compute_communication_rank_variance(f: list) -> float:
    n = int(math.log2(len(f)))
    if 2**n != len(f):
        raise ValueError("Input list length must be a power of 2")
    
    # Compute the indicator function for each bit position
    indicators = [sum(1 for x in f if (i >> j) & 1 == x) / len(f) for j in range(n)]
    
    # Compute the variance of the communication ranks
    mean_rank = sum(indicators)
    variance = sum((rank - mean_rank) ** 2 for rank in indicators) / n
    return variance

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        f = generate_random_boolean_function(n)
        c_g = compute_diophantine_equation_complexity(f)
        crv_f = compute_communication_rank_variance(f)
        results.append({"n": n, "c_g": c_g, "crv_f": crv_f})
    
    if not results:
        return {
            "metric_name": "Pearson's correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    c_g_values = [result["c_g"] for result in results]
    crv_f_values = [result["crv_f"] for result in results]
    
    if any(c_g > 10 for c_g in c_g_values):
        return {
            "metric_name": "Pearson's correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": False,
            "counterexample": f"c(g) > 10 for n={max(result['n'] for result in results)}"
        }
    
    correlation_coefficient = pearsons_correlation(c_g_values, crv_f_values)
    return {
        "metric_name": "Pearson's correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

def pearsons_correlation(x: list, y: list) -> float:
    n = len(x)
    if n != len(y):
        raise ValueError("Input lists must have the same length")
    
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    
    numerator = sum((x_i - mean_x) * (y_i - mean_y) for x_i, y_i in zip(x, y))
    denominator = math.sqrt(sum((x_i - mean_x) ** 2 for x_i in x)) * math.sqrt(sum((y_i - mean_y) ** 2 for y_i in y))
    
    if denominator == 0:
        return float('nan')
    
    return numerator / denominator

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = [2**i - 1 for i in range(5, 6)]  # Default to first few primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = len([r for r in results if "conjecture_holds" in r and r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if 'counterexample' in r)}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")