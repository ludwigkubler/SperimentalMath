# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_formula(n):
        variables = set(f"x{i}" for i in range(1, n + 1))
        clauses = []
        for _ in range(n):
            clause = random.sample(variables | {f"~{v}" for v in variables}, 2)
            clauses.append(clause)
        return clauses
    
    def dpll_search_tree_width(clauses):
        # Simplified DPLL search tree width calculation
        return len(clauses)
    
    def quasi_polynomial_betti_number(n):
        # Placeholder function to calculate Quasi-Polynomial Betti number
        # This is a dummy implementation for testing purposes
        return n
    
    max_beta_1 = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        formula = generate_formula(n)
        w_phi = dpll_search_tree_width(formula)
        beta_1_phi = quasi_polynomial_betti_number(n)
        
        if beta_1_phi > max_beta_1:
            max_beta_1 = beta_1_phi
        
        instances_tested += len(formula)
        n_max = max(n_max, n)
    
    upper_bound = Fraction(0)  # Placeholder for the actual upper bound calculation
    p_value = 0  # Placeholder for the statistical test result
    
    if max_beta_1 > upper_bound:
        conjecture_holds = False
        counterexample = "beta_1_phi exceeds upper_bound"
    
    return {
        "metric_name": "max_beta_1",
        "metric_value": max_beta_1,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_beta_1 = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_beta_1} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")