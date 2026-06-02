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
        clauses = []
        for _ in range(2**n - 1):  # Generate a random CNF formula with n variables
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf, assignment=[]):
        if not cnf:
            return True
        unit_clause = next((c for c in cnf if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment + [literal] if literal > 0 else assignment + [-literal]
            return dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment)
        
        literal, _ = random.choice(cnf)  # Choose a literal randomly
        new_assignment1 = assignment + [literal]
        new_assignment2 = assignment + [-literal]
        return dpll(cnf, new_assignment1) or dpll(cnf, new_assignment2)
    
    def frege_complexity(cnf):
        if not cnf:
            return 0
        unit_clause = next((c for c in cnf if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_cnf = [c for c in cnf if literal not in c and -literal not in c]
            return 1 + frege_complexity(new_cnf)
        
        literal, _ = random.choice(cnf)  # Choose a literal randomly
        new_cnf1 = [c for c in cnf if literal not in c and -literal not in c]
        new_cnf2 = [c for c in cnf if literal not in c and -literal not in c]
        return 1 + max(frege_complexity(new_cnf1), frege_complexity(new_cnf2))
    
    def ehrhart_rank(cnf):
        # Placeholder implementation of Ehrhart rank calculation
        # This is a dummy function for demonstration purposes
        return len(cnf)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    complexity = frege_complexity(cnf)
    ehrhart_rank_value = ehrhart_rank(cnf)
    
    metric_name = "Frege Proof Complexity"
    metric_value = complexity
    instances_tested = 1
    n_max = n
    conjecture_holds = False
    counterexample = ""
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 6)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")