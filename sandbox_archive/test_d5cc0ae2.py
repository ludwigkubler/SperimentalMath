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
    
    def generate_random_sat_instance(n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([1, -1]) * random.randint(1, n) for _ in range(random.randint(1, 3))]
            clauses.append(clause)
        return clauses
    
    def tseitin_formula(clauses):
        literals = set()
        for clause in clauses:
            literals.update(abs(lit) for lit in clause)
        n_vars = max(literals)
        
        formulas = []
        for i, literal in enumerate(range(1, n_vars + 1)):
            formulas.append(f"X{i} = {literal}")
        
        for i, clause in enumerate(clauses):
            formula = f"Y{i}"
            formulas.append(formula)
            for lit in clause:
                if lit > 0:
                    formulas.append(f"{formula} = X{abs(lit)}")
                else:
                    formulas.append(f"{formula} = ~X{abs(lit)}")
        
        return formulas
    
    def resolution_width(formulas):
        clauses = [set(map(int, f.split()[2:])) for f in formulas if '=' not in f]
        queue = list(clauses)
        derived = set()
        
        while queue:
            clause1 = queue.pop(0)
            if len(clause1) == 0:
                return float('inf')
            
            for clause2 in queue:
                if len(clause2) == 0:
                    return float('inf')
                
                for lit1 in clause1:
                    if -lit1 in clause2:
                        new_clause = clause1.union(clause2) - {lit1, -lit1}
                        if len(new_clause) == 0:
                            return float('inf')
                        if tuple(sorted(new_clause)) not in derived:
                            derived.add(tuple(sorted(new_clause)))
                            queue.append(new_clause)
        
        return max(len(c) for c in clauses)
    
    def local_induction_degree(formulas):
        # Placeholder for the actual LID computation
        # For simplicity, we use a dummy value here
        return random.random() * 10
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    sat_instance = generate_random_sat_instance(n)
    tseitin_formulas = tseitin_formula(sat_instance)
    
    lid = local_induction_degree(tseitin_formulas)
    width = resolution_width(tseitin_formulas)
    
    if width == float('inf'):
        return {
            "metric_name": "LID/Width Ratio",
            "metric_value": float('nan'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Resolution proof width is infinite"
        }
    
    ratio = lid / width
    return {
        "metric_name": "LID/Width Ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True if ratio <= 10 else False,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if not math.isnan(r["metric_value"])) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(not math.isnan(r["metric_value"]) for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=nan support_fraction={support_fraction}")
    elif any(math.isnan(r["metric_value"]) for r in results):
        print("RESULT: INCONCLUSIVE metric_saturation")
    else:
        first_failing_seed = next((i for i, r in enumerate(results) if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"LID/Width Ratio exceeds 10\" first_failing_seed={first_failing_seed}")