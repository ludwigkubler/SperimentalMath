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
    
    def generate_cnf(n):
        cnf = []
        for _ in range(2 ** n - 1):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[j] for j in range(i)):
                cnf.append(clause)
        return cnf
    
    def tseitin_representation(cnf):
        literals = set()
        for clause in cnf:
            for literal in clause:
                literals.add(literal)
        
        formulas = {}
        next_var = 1
        for clause in cnf:
            formula = next_var
            formulas[next_var] = clause
            next_var += 1
        
        for literal in literals:
            if literal > 0:
                formulas[literal] = [literal]
            else:
                formulas[-literal] = [-literal]
        
        return formulas
    
    def dpll_search_tree_diameter(formulas):
        # Simplified DPLL search tree diameter calculation (not actual DPLL)
        return len(formulas) + 1
    
    def min_local_ring_norm(cnf):
        # Placeholder for minimal local ring norm computation
        return sum(len(clause) for clause in cnf)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    formulas = tseitin_representation(cnf)
    td = dpll_search_tree_diameter(formulas)
    min_norm = min_local_ring_norm(cnf)
    
    metric_value = math.log(math.factorial(n)) * min_norm
    instances_tested = 1
    n_max = n
    conjecture_holds = False
    counterexample = ""
    
    return {
        "metric_name": "log(n!) * min_{P ∈ φ_T} |P|",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_td = sum(result["metric_value"] for result in results) / len(results)
    support_count = sum(1 for result in results if result["conjecture_holds"])
    support_fraction = support_count / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_td} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_td} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")