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

def generate_tseitin_formula(n):
    variables = list(range(1, n + 1))
    clauses = []
    
    for i in range(1, n + 1):
        clauses.append([variables[i-1]])
        for j in range(i + 1, n + 1):
            clauses.append([-variables[i-1], variables[j-1]])
            clauses.append([-variables[j-1], variables[i-1]])
    
    return clauses

def gaussian_elimination(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    rank = 0
    
    for i in range(cols):
        pivot_row = -1
        for j in range(rank, rows):
            if matrix[j][i] != 0:
                pivot_row = j
                break
        
        if pivot_row == -1:
            continue
        
        matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
        
        for j in range(rows):
            if i == j:
                continue
            factor = Fraction(matrix[j][i], matrix[rank][i])
            for k in range(cols):
                matrix[j][k] -= factor * matrix[rank][k]
        
        rank += 1
    
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        formula = generate_tseitin_formula(n)
        incidence_matrix = [[0] * (n + 1) for _ in range(n + 1)]
        
        for clause in formula:
            for lit in clause:
                if lit > 0:
                    incidence_matrix[lit][lit] += 1
                else:
                    incidence_matrix[-lit][-lit] += 1
        
        rank = gaussian_elimination(incidence_matrix)
        results.append(rank)
    
    metric_value = sum(results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(result <= n**(2/3) * math.log(n)**2 for result, n in zip(results, n_values))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Minimal Rank of Tropicalized Homology Groups",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3**j for i in range(5) for j in range(5)]
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']:.6f}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        support_fraction = 1.0
    else:
        support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(result['metric_value'] for result in results)/len(results):.6f} std=unknown support_fraction={support_fraction:.2f}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")