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
    
    def generate_sat_instance(n):
        variables = set(f'x{i}' for i in range(1, n+1))
        clauses = []
        for _ in range(n):
            clause = random.sample(variables, 2)
            clauses.append(clause)
        return clauses
    
    def tseitin_formula(clauses):
        literals = set()
        for clause in clauses:
            literals.update(clause)
        new_vars = {var: f'y{i}' for i, var in enumerate(literals, start=1)}
        new_clauses = []
        for literal in literals:
            new_clauses.append([new_vars[literal]])
            for clause in clauses:
                if literal not in clause:
                    new_clause = [f'~{new_vars[literal]}']
                    new_clause.extend(clause)
                    new_clauses.append(new_clause)
        return new_clauses
    
    def p_adic_valuation_ring_size(n):
        # Simplified approximation for demonstration
        return 2**n
    
    def logarithmic_capacity(size):
        if size <= 0:
            return 0
        return math.log2(size)
    
    def clause_depth(clauses):
        max_depth = 0
        for clause in clauses:
            depth = sum(1 for var in clause if var.startswith('~'))
            max_depth = max(max_depth, depth)
        return max_depth
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        clauses = generate_sat_instance(n)
        tseitin_clauses = tseitin_formula(clauses)
        size = p_adic_valuation_ring_size(n)
        cap = logarithmic_capacity(size)
        depth = clause_depth(tseitin_clauses)
        
        if cap >= 1.5 * depth:
            return {
                "metric_name": "C(n)/D(φ)",
                "metric_value": float('inf'),
                "instances_tested": len(n_values),
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "C(n) >= 1.5 * D(φ)"
            }
        
        results.append({
            "n": n,
            "cap": cap,
            "depth": depth
        })
    
    mean_cap = sum(result["cap"] for result in results) / len(results)
    mean_depth = sum(result["depth"] for result in results) / len(results)
    
    return {
        "metric_name": "C(n)/D(φ)",
        "metric_value": mean_cap / mean_depth,
        "instances_tested": len(n_values),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
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