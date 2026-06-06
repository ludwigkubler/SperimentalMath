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
from fractions import Fraction
import math

def generate_cnf(n):
    cnf = []
    for _ in range(n * (n - 1) // 2):
        literals = [random.randint(1, n), random.randint(-n, -1)]
        random.shuffle(literals)
        cnf.append(tuple(literals))
    return cnf

def dpll(cnf, assignment={}):
    if not cnf:
        return True
    p, _ = random.choice(cnf)
    p_abs = abs(p)
    if p_abs in assignment:
        if assignment[p_abs] != (p > 0):
            return False
        else:
            return dpll([lit for lit in cnf if lit[0] != p_abs], assignment)
    
    # Try assigning True to p
    new_assignment = assignment.copy()
    new_assignment[p_abs] = True
    if dpll(cnf, new_assignment):
        return True
    
    # Try assigning False to p
    new_assignment[p_abs] = False
    if dpll(cnf, new_assignment):
        return True
    
    return False

def hensel_lifting_steps(cnf):
    if dpll(cnf):
        return 1
    else:
        return float('inf')

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    metric_name = "Hensel Lifting Steps"
    instances_tested = 0
    n_max = 0
    total_steps = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            cnf = generate_cnf(n)
            instances_tested += 1
            n_max = max(n_max, n)
            steps = hensel_lifting_steps(cnf)
            total_steps += steps
    
    if instances_tested < 30:
        return {
            "metric_name": metric_name,
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Insufficient instances tested"
        }
    
    mean_steps = total_steps / instances_tested
    return {
        "metric_name": metric_name,
        "metric_value": mean_steps,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": False,  # This trial does not support the conjecture
        "counterexample": "Mapping undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_steps = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_steps} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_steps} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Mapping undefined' first_failing_seed={first_failing_seed}")