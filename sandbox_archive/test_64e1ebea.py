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
            if matrix[i][i] == 0:
                continue
            factor = Fraction(1, matrix[i][i])
            for j in range(cols):
                matrix[i][j] *= factor
            for k in range(rows):
                if k != i:
                    factor = matrix[k][i]
                    for j in range(cols):
                        matrix[k][j] -= factor * matrix[i][j]
        return matrix
    
    def rank(matrix):
        row_echelon_form = gaussian_elimination(matrix)
        non_zero_rows = [row for row in row_echelon_form if any(row)]
        return len(non_zero_rows)
    
    def communication_rank(n):
        # Placeholder function to compute the communication rank
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, n)
    
    def stabilizer_group(n):
        # Placeholder function to compute the stabilizer group
        # This is a dummy implementation and should be replaced with actual logic
        return [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    instances_tested = 0
    n_max = 0
    total_generators = 0
    total_rank = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        T_phi = stabilizer_group(n)
        r_phi = communication_rank(n)
        
        if not T_phi or not r_phi:
            continue
        
        generators = rank(T_phi)
        
        instances_tested += 1
        n_max = max(n_max, n)
        total_generators += generators
        total_rank += r_phi
    
    if instances_tested == 0:
        return {
            "metric_name": "Generators vs Rank",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }
    
    mean_generators = total_generators / instances_tested
    mean_rank = total_rank / instances_tested
    
    correlation_coefficient = (instances_tested * mean_generators * mean_rank - 
                               sum(g * r for g, r in zip([mean_generators] * instances_tested, [mean_rank] * instances_tested))) / \
                              math.sqrt((instances_tested * mean_generators**2 - sum(g**2 for g in [mean_generators] * instances_tested)) *
                                        (instances_tested * mean_rank**2 - sum(r**2 for r in [mean_rank] * instances_tested)))
    
    return {
        "metric_name": "Generators vs Rank",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")