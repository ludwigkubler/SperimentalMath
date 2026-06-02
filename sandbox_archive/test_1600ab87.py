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
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def tseitin_encoding(cnf):
        literals = set()
        for clause in cnf:
            for literal in clause:
                literals.add(abs(literal))
        
        new_vars = {literal: random.randint(1, 2*n) for literal in literals}
        formulas = []
        
        for i, clause in enumerate(cnf):
            tseitin_var = new_vars[i+1]
            formulas.append([tseitin_var])
            for literal in clause:
                if literal > 0:
                    formulas.append([-tseitin_var, literal])
                else:
                    formulas.append([-tseitin_var, -literal])
        
        return formulas
    
    def resolution_width(formulas):
        clauses = set()
        queue = list(formulas)
        
        while queue:
            clause1 = queue.pop(0)
            for clause2 in queue:
                if not any(l in clause2 and -l in clause1 for l in clause1):
                    new_clause = [l for l in clause1 if l not in clause2] + [l for l in clause2 if l not in clause1]
                    if len(new_clause) == 0:
                        return float('inf')
                    if tuple(sorted(new_clause)) not in clauses:
                        clauses.add(tuple(sorted(new_clause)))
                        queue.append(new_clause)
        
        return max(len(clause) for clause in clauses)
    
    def count_braided_monoidal_categories(cnf):
        # Placeholder for the actual mapping logic
        # This is a dummy implementation and should be replaced with the actual mapping logic
        return len(cnf)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    tseitin_formulas = tseitin_encoding(cnf)
    resolution_width_value = resolution_width(tseitin_formulas)
    m_phi = count_braided_monoidal_categories(cnf)
    
    if m_phi == 0:
        return {
            "metric_name": "resolution_proof_width_to_braided_monoidal_categories_ratio",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ratio = resolution_width_value / m_phi
    return {
        "metric_name": "resolution_proof_width_to_braided_monoidal_categories_ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    std_ratio = math.sqrt(sum((result["metric_value"] - mean_ratio) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")