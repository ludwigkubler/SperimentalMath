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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0], clause[1] = clause[1], clause[0]
            cnf.append(clause)
        return cnf
    
    def construct_quandle(cnf):
        quandle = {}
        for clause in cnf:
            for lit in clause:
                if abs(lit) not in quandle:
                    quandle[abs(lit)] = set()
                quandle[abs(lit)].add((lit > 0, clause))
        return quandle
    
    def measure_non_trivial_entanglements(quandle):
        entanglements = 0
        for _, clauses in quandle.items():
            if len(clauses) > 1:
                entanglements += 1
        return entanglements
    
    def measure_dpll_search_tree_size(cnf):
        assignment = {}
        
        def search(depth):
            if all(lit in assignment or -lit in assignment for lit in sum(cnf, [])):
                return depth
            literal = next((lit for lit in range(1, max([abs(l) for l in sum(cnf, [])]) + 1) if lit not in assignment and -lit not in assignment), None)
            if literal is None:
                return float('inf')
            assignment[literal] = True
            max_depth_true = search(depth + 1)
            del assignment[literal]
            assignment[-literal] = True
            max_depth_false = search(depth + 1)
            del assignment[-literal]
            return max(max_depth_true, max_depth_false)
        
        return search(0)
    
    def linear_regression(x, y):
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_xx = sum(xi ** 2 for xi in x)
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x ** 2)
        intercept = (sum_y - slope * sum_x) / n
        r_squared = (n * sum_xy - sum_x * sum_y) ** 2 / ((n * sum_xx - sum_x ** 2) * (n * sum_yy - sum_y ** 2))
        
        return slope, intercept, r_squared
    
    cnf = generate_cnf(10, 30)
    quandle = construct_quandle(cnf)
    entanglements = measure_non_trivial_entanglements(quandle)
    dpll_size = measure_dpll_search_tree_size(cnf)
    
    if dpll_size == float('inf'):
        return {
            "metric_name": "R²",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": 10,
            "conjecture_holds": False,
            "counterexample": "DPLL search tree size is infinite"
        }
    
    slope, intercept, r_squared = linear_regression([entanglements], [dpll_size])
    
    return {
        "metric_name": "R²",
        "metric_value": r_squared,
        "instances_tested": 1,
        "n_max": 10,
        "conjecture_holds": r_squared >= 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_r_squared = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["metric_value"] is not None and r["metric_value"] >= 0.9 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_r_squared} std=0 support_fraction={support_fraction}")
    elif any(r["conjecture_holds"] == False for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"R² below 0.9\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")