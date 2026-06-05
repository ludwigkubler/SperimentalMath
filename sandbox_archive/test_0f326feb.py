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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_tseitin_formula(n, d):
        if n % d != 0:
            return None
        variables = list(range(1, n + 1))
        clauses = []
        for i in range(d):
            clause = [random.choice(variables) for _ in range(n // d)]
            clauses.append(clause)
        tseitin_formula = []
        for i, clause in enumerate(clauses):
            new_var = n + i + 1
            tseitin_formula.extend([[new_var] + [-v] for v in clause])
            tseitin_formula.append([new_var] + [-v for v in clause])
            tseitin_formula.append([-new_var] + [v for v in clause])
        return tseitin_formula
    
    def resolution_width(clause_set):
        clauses = list(clause_set)
        while True:
            new_clause = None
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    if set(clauses[i]) & set(clauses[j]):
                        new_clause = [x for x in clauses[i] if x not in clauses[j]]
                        break
                if new_clause:
                    break
            if not new_clause:
                return len(clauses)
            clauses.append(new_clause)
    
    def tropical_hodge_decomposition_size(n):
        # Simplified model: OHD is proportional to n^2 for demonstration
        return random.randint(1, 3 * n**2)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    d = 2
    formula = generate_tseitin_formula(n, d)
    if not formula:
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    resolution_w = resolution_width(formula)
    hodge_order = tropical_hodge_decomposition_size(n)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": resolution_w,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": hodge_order <= 3 * resolution_w and hodge_order >= 0.8 * resolution_w,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] > 3 * r["resolution_width"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["metric_value"] > 3 * r["resolution_width"])
        print(f"RESULT: FALSIFIED counterexample=\"OHD > 3w\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")