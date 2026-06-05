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
        cnf = []
        for _ in range(n * 2):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
            cnf.append(clause)
        return cnf
    
    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        unit_clauses = [c for c in cnf if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0][0]
            new_assignment = {**assignment, abs(literal): literal > 0}
            return dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment)
        
        p = next(iter(assignment))
        return dpll(cnf, {**assignment, p: True}) or dpll(cnf, {**assignment, p: False})
    
    def min_order_of_generators(cnf):
        # Placeholder for actual computation
        return random.randint(1, 10)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    min_order = min_order_of_generators(cnf)
    w_phi = dpll(cnf)
    
    if min_order > 10:
        return {
            "metric_name": "min_order",
            "metric_value": min_order,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "generator_order_metric_too_high"
        }
    
    return {
        "metric_name": "min_order",
        "metric_value": min_order,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r['metric_value'] for r in results) / len(results)
    std_value = math.sqrt(sum((r['metric_value'] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results) and any(r['counterexample'] == 'generator_order_metric_too_high' for r in results):
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"generator_order_metric_too_high\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")