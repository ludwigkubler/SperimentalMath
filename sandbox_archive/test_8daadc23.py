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

def generate_tropical_curve(r):
    # Generate a tropical curve with rank r
    return [random.randint(1, 2) for _ in range(r)]

def construct_tseitin_formula(curve):
    # Construct a Tseitin formula from the tropical curve
    n = len(curve)
    variables = list(range(n))
    clauses = []
    
    for i in range(n):
        if curve[i] == 1:
            clauses.append([variables[i]])
        else:
            clauses.append([-variables[i]])
    
    return clauses

def resolution_depth(formula):
    # Compute the resolution depth of the Tseitin formula
    n = len(formula)
    queue = []
    resolved = [False] * n
    
    for i in range(n):
        if not any(x < 0 for x in formula[i]):
            queue.append(i)
    
    depth = 0
    while queue:
        new_queue = []
        for i in queue:
            for j in range(n):
                if all(x >= 0 for x in formula[j]) and any(x == -formula[i][k] for k in range(len(formula[i]))):
                    new_formula = [x for x in formula[j] if x != -formula[i][k]]
                    if not any(new_formula[k] < 0 for k in range(len(new_formula))):
                        resolved[j] = True
                    else:
                        new_queue.append(j)
        queue = new_queue
        depth += 1
    
    return depth

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        curve = generate_tropical_curve(n)
        formula = construct_tseitin_formula(curve)
        depth = resolution_depth(formula)
        
        if depth < 2**n:
            return {
                "metric_name": "resolution_depth",
                "metric_value": depth,
                "instances_tested": n,
                "conjecture_holds": False,
                "counterexample": f"Curve rank {n}, expected depth >= {2**n}, got {depth}"
            }
        
        results.append(depth)
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    support_fraction = len([x for x in results if x >= 2**n]) / len(results)
    
    return {
        "metric_name": "resolution_depth",
        "metric_value": mean,
        "instances_tested": sum(len(generate_tropical_curve(n)) for n in [5, 10, 15, 20, 30, 40]),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        if not result["conjecture_holds"]:
            break
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    support_fraction = len([x for x in results if x >= 2**n]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Curve rank {n}, expected depth >= {2**n}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")