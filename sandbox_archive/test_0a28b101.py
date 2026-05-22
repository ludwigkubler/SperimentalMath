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

def generate_polynomial(n):
    coefficients = [random.randint(0, 10) for _ in range(n + 1)]
    return lambda x: sum(c * (x ** i) for i, c in enumerate(coefficients))

def generate_acc0_circuit(f, n):
    inputs = [i for i in range(-n, n + 1)]
    outputs = f(inputs)
    acc0_circuit_size = len(outputs)
    return acc0_circuit_size

def tropical_matrix_rank(matrix):
    m, n = len(matrix), len(matrix[0])
    rank = 0
    for col in range(n):
        pivot_row = None
        for row in range(m):
            if matrix[row][col] != float('-inf'):
                pivot_row = row
                break
        if pivot_row is not None:
            rank += 1
            for i in range(m):
                if i != pivot_row and matrix[i][col] != float('-inf'):
                    factor = matrix[i][col] / matrix[pivot_row][col]
                    for j in range(n):
                        matrix[i][j] -= factor * matrix[pivot_row][j]
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    
    for n in n_values:
        f = generate_polynomial(n)
        acc0_circuit_size = generate_acc0_circuit(f, n)
        
        if acc0_circuit_size == 0:
            continue
        
        matrix = [[float('-inf')] * (n + 1) for _ in range(acc0_circuit_size)]
        for i in range(acc0_circuit_size):
            x = i - acc0_circuit_size // 2
            y = f(x)
            matrix[i][x] = y
        
        rank = tropical_matrix_rank(matrix)
        
        if rank == 0:
            continue
        
        instances_tested += 1
        total_metric_value += rank / acc0_circuit_size
    
    if instances_tested == 0:
        return {
            "metric_name": "rank_ratio",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "no_valid_instances"
        }
    
    mean_metric_value = total_metric_value / instances_tested
    conjecture_holds = mean_metric_value >= 1
    
    return {
        "metric_name": "rank_ratio",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "not_enough_evidence"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_evidence\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")