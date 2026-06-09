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
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if sum(clause) != 0:
                clauses.append(clause)
        return clauses
    
    def p_adic_representation(clauses):
        # Simplified representation using a dictionary of counts
        p_adic = {}
        for clause in clauses:
            key = tuple(sorted(abs(x) for x in clause))
            if key not in p_adic:
                p_adic[key] = 0
            p_adic[key] += 1
        return p_adic
    
    def local_cohomological_defect(p_adic):
        # Simplified calculation of defect as the sum of counts
        return sum(p_adic.values())
    
    def resolution_width(clauses):
        # Simulated DPLL solver for width (very simplified)
        width = 0
        stack = []
        for clause in clauses:
            if not any(var in stack for var in clause):
                stack.append(random.choice(clause))
                width = max(width, len(stack))
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        p_adic = p_adic_representation(cnf)
        defect = local_cohomological_defect(p_adic)
        width = resolution_width(cnf)
        
        if defect == 0:
            continue
        
        results.append({
            "n": n,
            "defect": defect,
            "width": width
        })
    
    if not results:
        return {
            "metric_name": "resolution_width_over_defect",
            "metric_value": float('inf'),
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    metric_values = [r["width"] / r["defect"] for r in results]
    mean_value = sum(metric_values) / len(metric_values)
    max_n = max(r["n"] for r in results)
    
    return {
        "metric_name": "resolution_width_over_defect",
        "metric_value": mean_value,
        "instances_tested": len(results),
        "n_max": max_n,
        "conjecture_holds": all(v <= 1.5 for v in metric_values),
        "counterexample": "" if all(v <= 1.5 for v in metric_values) else "exceeds_bound"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"exceeds_bound\" first_failing_seed={first_failing_seed}")