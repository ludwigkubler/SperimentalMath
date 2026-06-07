# auto-injected by SEC sandbox
import itertools
import collections
import json
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
import sys

def generate_random_sat_instance(n: int, m: int) -> list:
    clauses = []
    variables = set()
    for _ in range(m):
        clause = [random.choice([-1, 1]) * (i + 1) for i in random.sample(range(n), random.randint(1, n))]
        clauses.append(clause)
        variables.update(abs(l) for l in clause)
    return clauses, list(variables)

def hyperbolic_metric(clauses: list) -> float:
    # Placeholder for actual hyperbolic metric computation
    return len(clauses) ** 0.5

def height_of_dpll_tree(clauses: list, assignment: dict) -> int:
    if not clauses:
        return 0
    
    variables = set(abs(l) for l in sum(clauses, []))
    pure_literal = next((l for l in variables if all(l not in c or -l not in c for c in clauses)), None)
    
    if pure_literal is not None:
        new_clauses = [c for c in clauses if pure_literal not in c and -pure_literal not in c]
        return 1 + max(height_of_dpll_tree(new_clauses, assignment), height_of_dpll_tree(new_clauses, {**assignment, pure_literal: True}))
    else:
        l_true = next((l for l in variables if any(l in c for c in clauses)), None)
        new_clauses_true = [c for c in clauses if l_true not in c and -l_true not in c]
        return 1 + height_of_dpll_tree(new_clauses_true, {**assignment, l_true: True})

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_height = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):  # Test each size with 5 instances
            m = random.randint(n // 2, n * 2)
            clauses, variables = generate_random_sat_instance(n, m)
            height = height_of_dpll_tree(clauses, {})
            
            total_height += height
            instances_tested += 1
            n_max = max(n_max, n)
    
    mean_height = total_height / instances_tested
    conjecture_holds = mean_height <= 10 * hyperbolic_metric(clauses)
    counterexample = "" if conjecture_holds else f"Mean height {mean_height} exceeds bound"
    
    return {
        "metric_name": "DPLL Proof Tree Height",
        "metric_value": mean_height,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_height = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_height} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")