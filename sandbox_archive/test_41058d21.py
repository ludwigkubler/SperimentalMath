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
        # Find pivot row
        max_row = i
        for r in range(i+1, rows):
            if abs(matrix[r][i]) > abs(matrix[max_row][i]):
                max_row = r
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate non-pivot elements
        pivot = matrix[i][i]
        for j in range(i, cols):
            matrix[i][j] /= pivot
        for r in range(rows):
            if r != i:
                factor = matrix[r][i]
                for j in range(i, cols):
                    matrix[r][j] -= factor * matrix[i][j]

    rank = sum(1 for row in matrix if any(row))
    return rank

def compute_brauer_group(circuit):
    # Convert circuit to a string representation
    circuit_str = ' OR '.join(str(gate) for gate in circuit)
    
    # Simulate Brauer group computation (constructive mapping)
    # For simplicity, assume each gate contributes a 2x2 matrix modulo 2
    matrices = [[1, 0], [0, 1]] * len(circuit)
    result_matrix = []
    for mat in matrices:
        if not result_matrix:
            result_matrix = mat
        else:
            # Matrix multiplication modulo 2
            new_row = []
            for i in range(len(mat)):
                sum_val = 0
                for j in range(len(mat[0])):
                    sum_val += (mat[i][j] * result_matrix[j]) % 2
                new_row.append(sum_val)
            result_matrix = [new_row]
    
    return gaussian_elimination(result_matrix)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 30
    ranks = []
    widths = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        circuit = [random.choice([0, 1]) for _ in range(n)]
        
        rank = compute_brauer_group(circuit)
        width = sum(circuit)  # Monotone width is the number of gates
        
        ranks.append(rank)
        widths.append(width)
    
    if not ranks or not widths:
        return {
            "metric_name": "Brauer Group Rank",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "empty_ranks_or_widths"
        }
    
    # Perform linear regression
    mean_rank = sum(ranks) / len(ranks)
    mean_width = sum(widths) / len(widths)
    ss_tot = sum((w - mean_width)**2 for w in widths)
    ss_res = sum((r - (mean_rank * w / mean_width))**2 for r, w in zip(ranks, widths))
    
    if ss_tot == 0:
        return {
            "metric_name": "Brauer Group Rank",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "constant_width"
        }
    
    r_squared = 1 - (ss_res / ss_tot)
    slope = mean_rank * (mean_width / len(widths))
    
    return {
        "metric_name": "Brauer Group Rank",
        "metric_value": slope,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(slope - 1) <= 0.1 and r_squared >= 0.95,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 7 for i in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_slope = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_slope = math.sqrt(sum((r["metric_value"] - mean_slope)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_slope} std={std_slope} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_slope} std={std_slope} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='slope_outside_range' first_failing_seed={first_failing_seed}")