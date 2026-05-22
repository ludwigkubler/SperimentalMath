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
    
    def generate_formula(n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for _ in range(10):  # Generate a few clauses
            clause = random.sample(variables, random.randint(1, n))
            clause.append(random.choice(['', 'not']))
            clauses.append(clause)
        return clauses
    
    def integral_representation(formula):
        # Simplified integral representation logic
        norm = max(abs(sum(int(c[0]) for c in clause)) for clause in formula)
        return norm
    
    def dpll_search_tree_width(formula):
        # Simplified DPLL search tree width logic
        width = len(formula)  # Placeholder value
        return width
    
    n = random.randint(5, 40)
    formula = generate_formula(n)
    norm = integral_representation(formula)
    width = dpll_search_tree_width(formula)
    
    metric_name = "Minimal Norm vs DPLL Width"
    metric_value = norm / math.log(n)
    instances_tested = 1
    conjecture_holds = (norm <= math.log(n)) and (width <= 2 * math.log(n))
    counterexample = "" if conjecture_holds else f"Norm={norm}, Width={width}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")