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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf):
        assignment = {}
        
        def solve():
            unassigned_vars = [v for v in range(1, len(cnf) + 1) if v not in assignment and -v not in assignment]
            if not unassigned_vars:
                return all([any([assignment.get(l, False) for l in clause]) for clause in cnf])
            
            p = unassigned_vars[0]
            new_assignment[p] = True
            if solve():
                return True
            
            del new_assignment[p]
            new_assignment[-p] = True
            if solve():
                return True
            
            del new_assignment[-p]
            return False
        
        return solve()
    
    n_max = 40
    instances_tested = 0
    metric_values = []
    
    for n in range(5, n_max + 1):
        for _ in range(6):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n)
            path_length = dpll(cnf)
            if path_length is not None:
                instances_tested += 1
                metric_values.append(path_length)
    
    if instances_tested < 30:
        return {
            "metric_name": "DPLL Proof Path Length",
            "metric_value": -1,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    correlation_coefficient = calculate_correlation(metric_values, [i for i in range(5, n_max + 1)])
    
    return {
        "metric_name": "DPLL Proof Path Length",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

def calculate_correlation(x, y):
    if len(x) != len(y):
        return None
    
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    
    cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
    var_x = sum((x[i] - mean_x) ** 2 for i in range(n)) / n
    var_y = sum((y[i] - mean_y) ** 2 for i in range(n)) / n
    
    if var_x == 0 or var_y == 0:
        return None
    
    return cov_xy / (math.sqrt(var_x) * math.sqrt(var_y))

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] != -1) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] != -1) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seed}")
                break