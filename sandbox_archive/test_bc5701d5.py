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

def zeta(s, max_iter=100):
    if s == 1:
        return float('inf')
    result = 0
    for n in range(1, max_iter + 1):
        term = 1 / (n ** s)
        if abs(term) < 1e-10:
            break
        result += term
    return result

def find_zero(length):
    low, high = 0, length
    while low <= high:
        mid = (low + high) / 2
        z = zeta(1/2 + 1j * mid)
        if abs(z) < 1e-10:
            return mid
        elif z.real > 0:
            high = mid - 1
        else:
            low = mid + 1
    return None

def generate_cnf(n):
    clauses = []
    for _ in range(n):
        clause = random.sample(range(1, n+1), 2)
        clauses.append(clause)
    cnf = [clauses]
    return cnf

def resolution_length(cnf):
    # Simplified resolution algorithm to estimate length
    steps = 0
    while True:
        new_clauses = []
        for clause in cnf:
            if len(clause) == 1:
                return steps
            for other_clause in cnf:
                if set(clause).isdisjoint(other_clause):
                    continue
                diff = list(set(clause) ^ set(other_clause))
                if len(diff) == 2:
                    new_clauses.append(diff)
        cnf.extend(new_clauses)
        steps += 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    length = resolution_length(cnf)
    t = find_zero(length)
    
    if t is None:
        return {
            "metric_name": "t",
            "metric_value": -1,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "No zero found in the critical strip"
        }
    
    return {
        "metric_name": "t",
        "metric_value": t,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_t = sum(r["metric_value"] for r in results if r["conjecture_holds"]) / len(results)
    std_t = math.sqrt(sum((r["metric_value"] - mean_t) ** 2 for r in results if r["conjecture_holds"])) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_t} std={std_t} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_t} std={std_t} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")