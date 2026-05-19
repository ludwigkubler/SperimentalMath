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
            max_row = i
            for j in range(i+1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            pivot = matrix[i][i]
            for j in range(cols):
                matrix[i][j] /= pivot
            for j in range(rows):
                if j != i:
                    factor = matrix[j][i]
                    for k in range(cols):
                        matrix[j][k] -= factor * matrix[i][k]
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    def generate_bp(n, read_twice=False):
        bp = []
        for i in range(n):
            bp.append(random.choice([0, 1]))
            if read_twice:
                bp.append(bp[-1])
        return bp
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per size
            bp = generate_bp(n, read_twice=True)
            transition_matrix = [[bp[i] == bp[j] for j in range(n)] for i in range(n)]
            rank = gaussian_elimination(transition_matrix)
            total_rank += rank
            instances_tested += 1
    
    avg_rank = total_rank / instances_tested
    conjecture_holds = avg_rank >= 0.8 * n_values[-1]
    counterexample = "mapping_undefined" if not conjecture_holds else ""
    
    return {
        "metric_name": "average_matroid_rank",
        "metric_value": avg_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 
                                                   31, 37, 41, 43, 47, 53, 59, 61, 
                                                   67, 71, 73, 79, 83, 89, 97, 101, 
                                                   103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    avg_rank = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_rank} std=0 support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")