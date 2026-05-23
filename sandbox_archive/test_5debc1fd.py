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

def generate_cnf(n):
    clauses = []
    for _ in range(2 * n):
        clause = [random.randint(-n, -1), random.randint(1, n)]
        clauses.append(clause)
    return clauses

def dpll(cnf, assignment=None):
    if not cnf:
        return True
    if any(all(lit not in assignment for lit in clause) for clause in cnf):
        return False
    
    literal = None
    for lit in range(1, n + 1):
        if all(lit not in assignment and -lit not in assignment for clause in cnf):
            literal = lit
            break
    if literal is None:
        literal = random.choice([x for x in range(1, n + 1) if x not in assignment])
    
    new_assignment = assignment.copy()
    new_assignment[literal] = True
    if dpll(cnf, new_assignment):
        return True
    
    new_assignment[literal] = False
    if dpll(cnf, new_assignment):
        return True
    
    return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        width = len(dpll(cnf))
        alpha_H_n_squared = (n * (n + 1) // 2) ** 2
        
        results.append({
            "metric_name": "DPLL Search Tree Width",
            "metric_value": width,
            "instances_tested": 1,
            "conjecture_holds": width <= alpha_H_n_squared,
            "counterexample": "" if width <= alpha_H_n_squared else f"n={n}, width={width}, alpha(H_n)^2={alpha_H_n_squared}"
        })
    
    mean_width = sum(result["metric_value"] for result in results) / len(results)
    std_width = math.sqrt(sum((result["metric_value"] - mean_width) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "mean_width": mean_width,
        "std_width": std_width,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_width = sum(result["mean_width"] for result in results) / len(results)
    std_width = math.sqrt(sum((result["mean_width"] - mean_width) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["support_fraction"] == 1) / len(results)
    
    if all(result["support_fraction"] == 1 for result in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    elif any(result["support_fraction"] < 0.8 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["support_fraction"] < 0.8)
        print(f"RESULT: FALSIFIED counterexample='first failing seed' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")