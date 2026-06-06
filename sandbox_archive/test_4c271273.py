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
    
    def tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        
        # Create clauses for each variable being true
        for i in range(1, n+1):
            clauses.append(f'{variables[i-1]}')
        
        # Create clauses for each variable being false
        for i in range(1, n+1):
            clauses.append(f'-{variables[i-1]} {variables[-1]}')
        
        return clauses
    
    def sat_clause_subset_complexity(clauses):
        return len(clauses)
    
    def diophantine_system(clauses):
        # Placeholder for constructing the diophantine system
        # This is a dummy implementation and should be replaced with actual logic
        return []
    
    def minimal_order_of_equivalence_classes(diophantine_system):
        # Placeholder for computing the minimal order of equivalence classes
        # This is a dummy implementation and should be replaced with actual logic
        return 1
    
    n = random.randint(5, 40)
    clauses = tseitin_formula(n)
    sat_complexity = sat_clause_subset_complexity(clauses)
    diophantine_sys = diophantine_system(clauses)
    minimal_order = minimal_order_of_equivalence_classes(diophantine_sys)
    
    if sat_complexity == 0:
        return {
            "metric_name": "MinimalOrder",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "SATComplexity is zero"
        }
    
    ratio = minimal_order / sat_complexity
    
    return {
        "metric_name": "MinimalOrder",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(ratio - 1) <= 0.1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_ratio = sum(result["metric_value"] for result in results) / len(results)
        std_dev = math.sqrt(sum((result["metric_value"] - mean_ratio) ** 2 for result in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")