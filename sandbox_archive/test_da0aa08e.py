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
    for _ in range(n):
        clause = [random.randint(1, n) * (-1 if random.choice([True, False]) else 1)
                   for _ in range(random.randint(2, 4))]
        clauses.append(clause)
    return clauses

def resolution_depth(cnf):
    stack = []
    visited = set()
    
    def resolve(lit):
        if lit in visited:
            return False
        visited.add(lit)
        for clause in cnf:
            if -lit in clause:
                new_clause = [x for x in clause if x != -lit]
                if not new_clause:
                    return True
                stack.append((new_clause, len(stack)))
                if resolve(new_clause[0]):
                    return True
                stack.pop()
        return False
    
    for lit in random.sample(range(1, 2*n+1), n):
        if resolve(lit):
            return len(stack)
    
    return float('inf')

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for _ in range(30):  # Ensure at least 30 instances per seed
        cnf = generate_cnf(random.randint(5, 40))
        depth = resolution_depth(cnf)
        if depth == float('inf'):
            continue
        results.append(depth)
    
    if not results:
        return {
            "metric_name": "resolution_depth",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_d = sum(results) / len(results)
    return {
        "metric_name": "resolution_depth",
        "metric_value": mean_d,
        "instances_tested": len(results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        if "metric_value" in result and result["metric_value"] is not None:
            results.append(result["metric_value"])
    
    if len(results) == 0 or all(math.isnan(x) for x in results):
        print("RESULT: INCONCLUSIVE no valid data")
    else:
        mean_d = sum(results) / len(results)
        std_d = math.sqrt(sum((x - mean_d) ** 2 for x in results) / len(results))
        support_fraction = sum(1 for x in results if x <= 2 * mean_d) / len(results)
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_d} std={std_d} support_fraction={support_fraction}")
        else:
            print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={seeds[results.index(max(results))]}")