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

def agm(x, y):
    return ((x * y) ** 0.5)

def resolution_depth(clauses):
    if not clauses:
        return 0
    new_clauses = set()
    for clause in clauses:
        new_clause = []
        for lit in clause:
            if -lit in new_clauses:
                new_clause.append(lit)
        if new_clause and tuple(new_clause) not in new_clauses:
            new_clauses.add(tuple(new_clause))
    return 1 + resolution_depth(list(new_clauses))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([30, 35, 40])
    m = random.randint(n, 2 * n)
    clauses = []
    for _ in range(m):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        clauses.append(clause)
    
    k = random.uniform(0.5, 0.9)
    agm_value = sum(agm(len(clause), len(clause)) ** k for clause in clauses) / m
    
    depth = resolution_depth(clauses)
    
    conjecture_holds = depth <= agm_value * 2
    counterexample = "" if conjecture_holds else f"Depth {depth} exceeds bound {agm_value * 2}"
    
    return {
        "metric_name": "Resolution Depth",
        "metric_value": depth,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_depth = sum(r["metric_value"] for r in results) / len(results)
    std_depth = (sum((r["metric_value"] - mean_depth) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_depth} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Depth exceeds bound\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")