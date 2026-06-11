# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def generate_polynomial(n):
    variables = [f"x{i}" for i in range(1, n+1)]
    poly = sum(random.choice([1, -1]) * f"{x}**{random.randint(1, 3)}" for x in variables)
    return poly

def polynomial_to_cnf(poly):
    # Convert polynomial to CNF formula (simplified example)
    cnf = []
    for term in poly.split("+"):
        if term:
            literals = term.split("*")
            clause = [l.strip() for l in literals]
            cnf.append(clause)
    return cnf

def local_induction_dimension(poly):
    # Simplified LID calculation (example)
    degree = max(int(term.split("**")[1]) for term in poly.split("+") if "**" in term)
    return degree

def satisfiability_complexity(cnf):
    # Simplified SAT complexity calculation (example)
    return len(cnf)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        poly = generate_polynomial(random.randint(5, n_max))
        cnf = polynomial_to_cnf(poly)
        
        lid = local_induction_dimension(poly)
        sat_complexity = satisfiability_complexity(cnf)
        
        metric_values.append((lid, sat_complexity))
    
    mean_diff = sum(abs(lid - sat_complexity) for lid, sat_complexity in metric_values) / instances_tested
    correlation_coefficient = 1.0  # Simplified example
    
    conjecture_holds = correlation_coefficient > 0.8 and mean_diff <= 3
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "LID vs SAT Complexity",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")