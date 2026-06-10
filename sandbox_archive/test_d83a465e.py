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

def gaussian_elimination(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    
    for i in range(rows):
        # Find pivot
        max_row = i
        for k in range(i, rows):
            if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                max_row = k
        
        # Swap current row with the pivot row
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate non-zero elements below the pivot
        factor = matrix[i][i]
        for j in range(cols):
            matrix[i][j] /= factor
        
        for k in range(i + 1, rows):
            factor = matrix[k][i]
            for j in range(cols):
                if i == j:
                    matrix[k][j] = 0
                else:
                    matrix[k][j] -= factor * matrix[i][j]
    
    return matrix

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    instances_tested = 30
    total_metric_value = 0.0
    
    for _ in range(instances_tested):
        # Generate a random communication protocol matrix
        matrix = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        
        # Perform Gaussian elimination to find the rank of the matrix
        rank = sum(1 for row in gaussian_elimination(matrix) if any(row))
        
        total_metric_value += rank
    
    metric_name = 'rank'
    metric_value = total_metric_value / instances_tested
    n_max = n
    conjecture_holds = True
    counterexample = ''
    
    # Check the conjecture conditions
    if not (n <= 40 and metric_value <= math.log2(n)**2):
        conjecture_holds = False
        counterexample = 'mapping_undefined'
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r['metric_value'] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r['metric_value'] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")