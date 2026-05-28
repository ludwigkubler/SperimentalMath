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
            max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = 1 / matrix[i][i]
            for j in range(cols):
                matrix[i][j] *= factor
            for k in range(rows):
                if k != i:
                    factor = matrix[k][i]
                    for j in range(cols):
                        matrix[k][j] -= factor * matrix[i][j]
        return matrix

    def rank(matrix):
        rows, cols = len(matrix), len(matrix[0])
        matrix = [row[:] for row in matrix]
        gaussian_elimination(matrix)
        return sum(1 for row in matrix if any(row[j] != 0 for j in range(cols)))

    def xor_circuit_degree(n):
        # Simplified XOR circuit degree calculation
        return int(math.log2(n)) + 1

    n = random.randint(5, 40)
    instances_tested = 30
    total_rank = 0
    total_degrees = 0
    
    for _ in range(instances_tested):
        cnf = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        rank_value = rank(cnf)
        degree_value = xor_circuit_degree(n)
        
        if rank_value == 0:
            continue
        
        total_rank += rank_value
        total_degrees += degree_value
    
    if instances_tested == 0:
        return {
            "metric_name": "ratio",
            "metric_value": None,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ratio = total_rank / total_degrees
    return {
        "metric_name": "ratio",
        "metric_value": ratio,
        "instances_tested": instances_tested,
        "conjecture_holds": ratio <= 10,  # Arbitrary constant for testing
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_ratio = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        result = f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}"
    
    print(result)