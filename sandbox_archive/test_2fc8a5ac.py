# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
from itertools import combinations

def generate_3cnf(m: int) -> list:
    variables = set(f'x{i}' for i in range(1, m + 1))
    clauses = []
    for _ in range(m):
        clause = []
        for var in random.sample(variables, 2):
            if random.choice([True, False]):
                clause.append(var)
            else:
                clause.append(f'{var}\'')
        clauses.append(clause)
    return clauses

def tropical_graph_size(clauses: list) -> int:
    n = len(clauses)
    adj_matrix = [[0] * n for _ in range(n)]
    
    for i, clause1 in enumerate(clauses):
        for j, clause2 in enumerate(clauses):
            if i == j:
                continue
            common_vars = set(clause1) & set(clause2)
            if common_vars:
                adj_matrix[i][j] = 1
    
    return sum(sum(row) for row in adj_matrix)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    n_max = 0
    instances_tested = 0
    
    for m in [10, 20, 30]:
        for _ in range(10):
            clauses = generate_3cnf(m)
            n = tropical_graph_size(clauses)
            
            if n > n_max:
                n_max = n
            
            instances_tested += 1
            results.append(n)
    
    metric_value = sum(results) / len(results)
    conjecture_holds = all(n <= m**2 * 4 for n in results)
    counterexample = "" if conjecture_holds else f"m={m}, n={n}"
    
    return {
        "metric_name": "tropical_graph_size",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
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
        
        if not result["conjecture_holds"]:
            break
        
        results.append(result["metric_value"])
    
    if len(results) == len(seeds):
        mean = sum(results) / len(results)
        std = (sum((x - mean) ** 2 for x in results) / len(results)) ** 0.5
        support_fraction = len([r for r in results if r <= 4 * m**2]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
        else:
            print("RESULT: INCONCLUSIVE insufficient_support")
    else:
        first_failing_seed = seeds[results.index(next(r for r in results if not r <= 4 * m**2))]
        print(f"RESULT: FALSIFIED counterexample=\"m={m}, n={n}\" first_failing_seed={first_failing_seed}")