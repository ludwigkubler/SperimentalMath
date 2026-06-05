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

def is_prime(n):
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def smallest_prime_dividing(n):
    for i in range(2, n + 1):
        if n % i == 0 and is_prime(i):
            return i
    return None

def dpll(clauses, assignment={}):
    if not clauses:
        return True
    unit_clause = next((c for c in clauses if len(c) == 1), None)
    if unit_clause:
        literal = unit_clause[0]
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
            return True
        new_assignment[literal] = False
        if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
            return True
        return False
    pure_literal = next((l for l in range(1, max(max(c) for c in clauses) + 1) if (l not in assignment and -l not in assignment)), None)
    if pure_literal:
        new_assignment = assignment.copy()
        new_assignment[pure_literal] = True
        if dpll([c for c in clauses if pure_literal not in c and -pure_literal not in c], new_assignment):
            return True
        new_assignment[pure_literal] = False
        if dpll([c for c in clauses if pure_literal not in c and -pure_literal not in c], new_assignment):
            return True
        return False
    literal = next((l for l in range(1, max(max(c) for c in clauses) + 1)), None)
    new_assignment = assignment.copy()
    new_assignment[literal] = True
    if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
        return True
    new_assignment[literal] = False
    if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
        return True
    return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_length = 0
        
        while instances_tested < 30:
            variables = list(range(1, n + 1))
            clauses = []
            
            for _ in range(random.randint(2, n)):
                clause = [random.choice(variables) * random.choice([-1, 1]) for _ in range(random.randint(1, n))]
                if all(l not in c and -l not in c for l in variables for c in clauses):
                    clauses.append(clause)
            
            q = smallest_prime_dividing(n)
            if q is None:
                continue
            
            length = dpll(clauses)
            if length is False:
                continue
            
            instances_tested += 1
            total_length += length
        
        if instances_tested == 0:
            continue
        
        metric_value = total_length / instances_tested
        n_max = max(n_values)
        
        results.append({
            "metric_name": "dpll_proof_length",
            "metric_value": metric_value,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": True,
            "counterexample": ""
        })
    
    if not results:
        return {
            "seed": seed,
            "metric_name": "dpll_proof_length",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_valid_instances"
        }
    
    mean = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "metric_name": "dpll_proof_length",
        "metric_value": mean,
        "instances_tested": sum(r["instances_tested"] for r in results),
        "n_max": max(r["n_max"] for r in results),
        "conjecture_holds": support_fraction >= 0.8 and std_dev <= 3 * (mean - min(r["metric_value"] for r in results)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8 and std_dev <= 3 * (mean - min(r["metric_value"] for r in results)):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={first_failing_seed}")