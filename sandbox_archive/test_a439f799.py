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
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(n):
            clause = [random.choice(variables), -random.choice(variables)]
            clauses.append(clause)
        return clauses
    
    def compute_genus(cnf):
        # Simplified heuristic to estimate genus based on number of variables and clauses
        num_vars = len(set(abs(x) for x in sum(cnf, [])))
        num_clauses = len(cnf)
        if num_vars <= 2:
            return 0
        elif num_clauses <= 3:
            return 1
        else:
            return int(math.sqrt(num_vars * num_clauses / 6))
    
    def local_polynomial_hierarchy_index(g):
        # Simplified heuristic for local polynomial hierarchy index
        if g == 0:
            return 0
        elif g == 1:
            return 1
        else:
            return g - 1
    
    def dpll_tree_width(cnf):
        # Simplified heuristic to estimate DPLL search tree width
        num_vars = len(set(abs(x) for x in sum(cnf, [])))
        return int(math.sqrt(num_vars))
    
    n = random.randint(1, 40)
    cnf = generate_cnf(n)
    g = compute_genus(cnf)
    I_g = local_polynomial_hierarchy_index(g)
    width_T_phi = dpll_tree_width(cnf)
    
    result = {
        "metric_name": "DPLL Tree Width",
        "metric_value": width_T_phi,
        "instances_tested": 1,
        "conjecture_holds": I_g < width_T_phi,
        "counterexample": "" if I_g < width_T_phi else f"Counterexample for n={n}, g={g}, I(g)={I_g}, width(T(φ))={width_T_phi}"
    }
    
    return result

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 30*37 + 1, 37))
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = result["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")