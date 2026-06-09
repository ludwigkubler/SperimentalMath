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
        for i in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def dpll(cnf):
        assignment = {}
        
        def solve():
            unassigned_vars = [var for var in range(1, len(cnf) + 1) if var not in assignment and -var not in assignment]
            if not unassigned_vars:
                return all(all(lit in assignment and assignment[lit] == True for lit in clause) or any(lit in assignment and assignment[lit] == False for lit in clause) for clause in cnf)
            
            literal = unassigned_vars[0]
            new_assignment[literal] = True
            if solve():
                return True
            
            del new_assignment[literal]
            new_assignment[-literal] = True
            if solve():
                return True
            
            del new_assignment[-literal]
            return False
        
        return solve()
    
    def tropical_cyclotomic_polynomial(cnf):
        degree = 0
        coefficients = {}
        
        for clause in cnf:
            max_var = max(abs(lit) for lit in clause)
            if max_var > degree:
                degree = max_var
            
            for lit in clause:
                if lit not in coefficients:
                    coefficients[lit] = Fraction(1, 2 ** abs(lit))
                else:
                    coefficients[lit] += Fraction(1, 2 ** abs(lit))
        
        return degree, len(coefficients)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        cnf = generate_cnf(n)
        if not dpll(cnf):
            return {
                "metric_name": "tropical cyclotomic polynomial complexity",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": "unsatisfiable CNF"
            }
        
        degree, num_coeffs = tropical_cyclotomic_polynomial(cnf)
        total_metric_value += degree * math.log(n) + num_coeffs
        instances_tested += 1
        n_max = max(n_max, n)
    
    metric_value = total_metric_value / instances_tested
    
    return {
        "metric_name": "tropical cyclotomic polynomial complexity",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True if metric_value <= 2 * n_max * math.log(n_max) else False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='unsatisfiable CNF' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")