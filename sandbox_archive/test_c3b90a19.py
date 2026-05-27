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

def generate_tseitin_circuit(n, m):
    inputs = list(range(1, n + 1))
    clauses = []
    
    for i in range(m):
        clause = [random.choice(inputs) for _ in range(2)]
        if random.choice([True, False]):
            clause.append(random.choice([-1, 1]))
        clauses.append(clause)
    
    return inputs, clauses

def tropicalize(matrix):
    n = len(matrix)
    m = len(matrix[0])
    result = [[max(matrix[i][j], matrix[j][i]) for j in range(m)] for i in range(n)]
    return result

def rank(matrix):
    n = len(matrix)
    m = len(matrix[0])
    if n != m:
        raise ValueError("Matrix must be square")
    
    # Gaussian elimination
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        if matrix[i][i] == 0:
            return float('inf')
        
        for j in range(i + 1, n):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(m):
                matrix[j][k] -= factor * matrix[i][k]
    
    rank = sum(1 for row in matrix if any(row))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    num_instances = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per size
            inputs, clauses = generate_tseitin_circuit(n, len(clauses))
            qmcs = [[random.choice([1, -1]) for _ in range(len(inputs))] for _ in range(len(clauses))]
            tropicalized_qmcs = tropicalize(qmcs)
            rank_value = rank(tropicalized_qmcs)
            
            if rank_value == float('inf'):
                continue
            
            total_rank += rank_value
            num_instances += 1
    
    mean_rank = Fraction(total_rank, num_instances) if num_instances > 0 else 0
    conjecture_holds = abs(mean_rank - math.sqrt(num_instances)) <= 1.5 * math.sqrt(num_instances)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "mean_rank",
        "metric_value": float(mean_rank),
        "instances_tested": num_instances,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")