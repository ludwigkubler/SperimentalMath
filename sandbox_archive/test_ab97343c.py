# auto-injected by SEC sandbox
import math
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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_monotone_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def incidence_complex(circuit):
        n = len(circuit)
        complex_ = {i: [] for i in range(n + 1)}
        for i in range(n):
            for j in range(i + 1, n + 1):
                if all((circuit[i] & (1 << k)) == (circuit[j] & (1 << k)) for k in range(n)):
                    complex_[i].append(j)
                    complex_[j].append(i)
        return complex_
    
    def homology_dimension(complex_):
        n = len(complex_)
        if not complex_[0]:
            return 0
        boundary_matrix = [[0] * (n + 1) for _ in range(n)]
        for i in range(1, n + 1):
            for j in complex_[i - 1]:
                boundary_matrix[j][i] += 1
        
        def gaussian_elimination(matrix):
            rows, cols = len(matrix), len(matrix[0])
            rank = 0
            for col in range(cols):
                pivot_row = None
                for row in range(rank, rows):
                    if matrix[row][col]:
                        pivot_row = row
                        break
                if pivot_row is not None:
                    matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
                    rank += 1
                    for other_row in range(rows):
                        if other_row != rank - 1 and matrix[other_row][col]:
                            factor = matrix[other_row][col] / matrix[rank - 1][col]
                            for c in range(cols):
                                matrix[other_row][c] -= factor * matrix[rank - 1][c]
            return rank
        
        return n - gaussian_elimination(boundary_matrix)
    
    def minimal_local_induction_dimension(dimension):
        if dimension == 0:
            return 0
        return 2 ** (dimension - 1) - 1
    
    n = random.randint(5, 30)
    circuit = generate_monotone_function(n)
    complex_ = incidence_complex(circuit)
    homology_dim = homology_dimension(complex_)
    local_induction_dim = minimal_local_induction_dimension(homology_dim)
    
    return {
        "metric_name": "minimal_local_induction_dimension",
        "metric_value": local_induction_dim,
        "instances_tested": 1,
        "conjecture_holds": local_induction_dim <= n ** (0.5 + 0.1),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(2, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "minimal_local_induction_dimension is too small"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")