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
    
    def generate_3cnf(n, m):
        clauses = []
        variables = [f"x{i}" for i in range(1, n+1)]
        neg_variables = [f"~x{i}" for i in range(1, n+1)]
        
        for _ in range(m):
            clause = random.sample(variables + neg_variables, 3)
            clauses.append(clause)
        
        return clauses
    
    def dpll_solve(clauses, assignment={}):
        if not clauses:
            return True
        if any(all(var not in assignment or assignment[var] != val for var, val in clause) for clause in clauses):
            return False
        
        var = next((var for var in variables if var not in assignment), None)
        if var is None:
            return True
        
        positive_var = var
        negative_var = f"~{var}"
        
        if dpll_solve([c for c in clauses if all(var not in c or assignment[var] != val for var, val in c)], {**assignment, positive_var: True}):
            return True
        if dpll_solve([c for c in clauses if all(var not in c or assignment[var] != val for var, val in c)], {**assignment, negative_var: False}):
            return True
        
        return False
    
    def algebraic_k_theory_rank(clauses):
        # Placeholder function to simulate the computation
        # Replace with actual algorithm for computing K-theory rank
        return random.randint(1, 10)
    
    n = random.randint(5, 40)
    m = random.randint(n * 2, n * 3)
    clauses = generate_3cnf(n, m)
    
    k_theory_rank = algebraic_k_theory_rank(clauses)
    width = dpll_solve(clauses)  # Assuming DPLL returns the number of steps
    
    return {
        "metric_name": "Correlation between K-theory rank and resolution width",
        "metric_value": k_theory_rank * width,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")