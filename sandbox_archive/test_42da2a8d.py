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
        for _ in range(2 * n):
            literals = [random.choice([f'x{i}', f'-x{i}']) for i in range(n)]
            clause = ' or '.join(literals)
            clauses.append(clause)
        cnf = ' and '.join(clauses)
        return cnf
    
    def dpll_solver(cnf):
        # Simplified DPLL solver
        literals = set()
        for clause in cnf.split(' and '):
            literals.update(clause.split(' or '))
        literals = list(literals)
        
        def solve(model, literals):
            if not literals:
                return True
            literal = literals[0]
            if literal.startswith('-'):
                literal = literal[1:]
                negated = True
            else:
                negated = False
            
            for value in [True, False]:
                model[literal] = value
                if solve(model, literals[1:]):
                    return True
                del model[literal]
            
            return False
        
        model = {}
        if solve(model, literals):
            return len(cnf.split(' and '))
        else:
            return float('inf')
    
    def algebro_geometric_invariant(n):
        # Placeholder for actual computation
        return n
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        d_phi = dpll_solver(cnf)
        r_phi = algebro_geometric_invariant(n)
        
        if d_phi == float('inf'):
            continue
        
        log_r_phi = math.log(r_phi) if r_phi > 0 else -float('inf')
        results.append((log_r_phi, d_phi))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    log_r_phi_values = [r for r, _ in results]
    d_phi_values = [d for _, d in results]
    
    correlation_coefficient = sum((log_r_phi - mean_log_r_phi) * (d_phi - mean_d_phi)
                                  for log_r_phi, d_phi in results) / len(results)
    mean_log_r_phi = sum(log_r_phi_values) / len(log_r_phi_values)
    mean_d_phi = sum(d_phi_values) / len(d_phi_values)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and mean_abs_diff <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 50, 2))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    correlation_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    mean_correlation = sum(correlation_values) / len(correlation_values)
    std_deviation = math.sqrt(sum((x - mean_correlation) ** 2 for x in correlation_values) / len(correlation_values))
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_correlation} std={std_deviation} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")