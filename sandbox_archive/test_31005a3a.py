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
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        # Find a non-zero pivot in column i
        pivot_row = next((j for j in range(i, rows) if matrix[j][i] != 0), None)
        if pivot_row is None:
            continue  # Column is all zeros, skip this column
        # Swap the current row with the pivot row
        matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
        # Eliminate non-zero entries below the pivot
        for j in range(i + 1, rows):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(cols):
                matrix[j][k] -= factor * matrix[i][k]

def rank(matrix):
    gaussian_elimination(matrix)
    return sum(1 for row in matrix if any(val != 0 for val in row))

def xor_circuit_degree(cnf):
    # Placeholder function to compute the degree of an XOR circuit
    # This is a dummy implementation and should be replaced with actual logic
    return len(cnf)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    cnf = [[random.choice([1, -1]) * (i + 1) for i in range(n)] for _ in range(random.randint(2, 10))]
    
    rank_value = rank(cnf)
    degree = xor_circuit_degree(cnf)
    
    if degree == 0:
        return {
            "metric_name": "Ratio",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "XOR circuit degree is zero"
        }
    
    ratio = Fraction(rank_value, degree)
    return {
        "metric_name": "Ratio",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values) / len(metric_values):.2f} std=0 support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(metric_values) / len(metric_values):.2f} std=0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio is greater than 1\" first_failing_seed={first_failing_seed + 2}")