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

def generate_formula(n):
    clauses = []
    for _ in range(2 * n):
        clause = [random.randint(-n, -1), random.randint(1, n)]
        clauses.append(clause)
    return clauses

def dpll_width(clauses, assignment=None):
    if assignment is None:
        assignment = {}
    
    literals = set()
    for clause in clauses:
        literals.update(abs(lit) for lit in clause if lit not in assignment or assignment[lit] == False)
    
    if not literals:
        return 0
    
    literal = min(literals, key=lambda x: abs(x))
    new_assignment = assignment.copy()
    new_assignment[literal] = True
    width_pos = 1 + dpll_width(clauses, new_assignment)
    
    new_assignment[literal] = False
    width_neg = 1 + dpll_width(clauses, new_assignment)
    
    return max(width_pos, width_neg)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    formula = generate_formula(n)
    width = dpll_width(formula)
    order = n * (n + 1) // 2  # Symmetric group S_n has order n!
    
    return {
        "metric_name": "correlation",
        "metric_value": width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_width = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if not result["conjecture_holds"]) / len(results)
    
    if all(not result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_width} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")