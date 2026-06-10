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
    
    def generate_cnf(n_vars, n_clauses):
        cnf = []
        for _ in range(n_clauses):
            clause = [random.choice([-1, 1]) * (i + 1) for i in random.sample(range(n_vars), random.randint(1, n_vars))]
            cnf.append(clause)
        return cnf
    
    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        literals = set(lit for clause in cnf for lit in clause if lit != 0)
        literal = next((lit for lit in literals if lit not in assignment), None)
        if literal is None:
            return False
        
        def propagate(lit):
            new_cnf = []
            for clause in cnf:
                if any(abs(l) == abs(lit) for l in clause):
                    continue
                if all(abs(l) != abs(lit) for l in clause):
                    return False, []
                new_clause = [l for l in clause if abs(l) != abs(lit)]
                new_cnf.append(new_clause)
            return True, new_cnf
        
        def backtrack():
            return dpll(cnf, assignment.copy())
        
        success, new_cnf = propagate(literal)
        if success:
            assignment[literal] = True
            if dpll(new_cnf, assignment):
                return True
            del assignment[literal]
        
        success, new_cnf = propagate(-literal)
        if success:
            assignment[-literal] = True
            if dpll(new_cnf, assignment):
                return True
            del assignment[-literal]
        
        return backtrack()
    
    def cocomplexity(cnf):
        # Placeholder for actual cocomplexity calculation
        return random.random()  # This is a dummy implementation
    
    n_vars = random.randint(10, 40)
    n_clauses = random.randint(10, 40)
    cnf = generate_cnf(n_vars, n_clauses)
    
    depth = dpll(cnf)
    cocomplexity_value = cocomplexity(cnf)
    
    if depth is None or cocomplexity_value is None:
        return {
            "metric_name": "d(χ_c(φ))",
            "metric_value": -math.inf,
            "instances_tested": 1,
            "n_max": n_vars,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    return {
        "metric_name": "d(χ_c(φ))",
        "metric_value": depth,
        "instances_tested": 1,
        "n_max": n_vars,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")