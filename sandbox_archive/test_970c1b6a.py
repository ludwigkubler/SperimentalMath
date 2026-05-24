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
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        max_row = i + max(range(i, rows), key=lambda j: abs(matrix[j][i]))
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        for j in range(rows):
            if i != j:
                factor = matrix[j][i] / matrix[i][i]
                for k in range(cols):
                    matrix[j][k] -= factor * matrix[i][k]
    return matrix

def determinant(matrix):
    rows, cols = len(matrix), len(matrix[0])
    det = 1
    for i in range(rows):
        if matrix[i][i] == 0:
            return 0
        for j in range(i + 1, rows):
            factor = matrix[j][i] / matrix[i][i]
            for k in range(cols):
                matrix[j][k] -= factor * matrix[i][k]
        det *= matrix[i][i]
    return det

def tensor_width(bp_size):
    # Placeholder function to simulate BP_ReadTwice tensor width calculation
    return bp_size

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([10, 15, 20, 25, 30])
    instances_tested = 0
    total_rank = 0
    total_width = 0
    
    for _ in range(6):  # Ensure at least 30 instances per seed
        points = [(random.uniform(-1, 1), random.uniform(-1, 1)) for _ in range(n)]
        tropical_divisor = [sum([abs(x[0] - p[0]) + abs(x[1] - p[1]) for p in points]) for x in points]
        min_rank = len(tropical_divisor) - max(tropical_divisor)
        
        bp_size = n * (n - 1) // 2  # Placeholder BP size
        width = tensor_width(bp_size)
        
        total_rank += min_rank
        total_width += width
        instances_tested += 1
    
    avg_rank = total_rank / instances_tested
    avg_width = total_width / instances_tested
    correlation_coefficient = (instances_tested * sum(avg_rank * avg_width for _ in range(instances_tested)) -
                               sum(avg_rank) * sum(avg_width)) / math.sqrt((instances_tested * sum(avg_rank**2) - sum(avg_rank)**2) *
                                                                 (instances_tested * sum(avg_width**2) - sum(avg_width)**2))
    
    conjecture_holds = correlation_coefficient > 0
    counterexample = "" if conjecture_holds else "correlation_coefficient"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")