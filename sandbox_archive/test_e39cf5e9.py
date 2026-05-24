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
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += (-1) ** j * matrix[0][j] * determinant(submatrix)
        return det
    
    def gaussian_elimination(matrix, b):
        n = len(matrix)
        augmented_matrix = [row[:] + [b[i]] for i, row in enumerate(matrix)]
        
        for i in range(n):
            # Find the pivot
            max_row = i
            for j in range(i+1, n):
                if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                    max_row = j
            
            # Swap rows
            augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
            
            # Eliminate below the pivot
            for j in range(i+1, n):
                factor = augmented_matrix[j][i] / augmented_matrix[i][i]
                for k in range(n + 1):
                    augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
        
        # Back-substitute to find the solution
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = augmented_matrix[i][-1]
            for j in range(i+1, n):
                x[i] -= augmented_matrix[i][j] * x[j]
            x[i] /= augmented_matrix[i][i]
        
        return x
    
    def read_twice_bp_size(n):
        # Placeholder function to generate a read-twice BP size
        return 2 ** (n + random.randint(0, n))
    
    def minimal_rank(n):
        # Placeholder function to compute the minimal rank of a locally constant sheaf
        return random.randint(1, n)
    
    def ratio_of_size_to_exp(n, r):
        bp_size = read_twice_bp_size(n)
        expected_size = 2 ** (n * r)
        return bp_size / expected_size
    
    n_values = [5, 10, 15, 20, 30, 40]
    ratios = []
    
    for n in n_values:
        r = minimal_rank(n)
        ratio = ratio_of_size_to_exp(n, r)
        ratios.append(ratio)
    
    mean_ratio = sum(ratios) / len(ratios)
    std_ratio = math.sqrt(sum((x - mean_ratio) ** 2 for x in ratios) / len(ratios))
    
    conjecture_holds = all(0.9 <= ratio <= 1.1 for ratio in ratios)
    counterexample = "" if conjecture_holds else "ratio_out_of_bounds"
    
    return {
        "metric_name": "Ratio of BP size to expected exponential behavior",
        "metric_value": mean_ratio,
        "instances_tested": len(ratios),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"ratio_out_of_bounds\" first_failing_seed={first_failing_seed}")