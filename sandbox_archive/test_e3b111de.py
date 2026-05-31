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
    
    def generate_tseitin_formula(n):
        # Generate a Tseitin formula with n variables
        var = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(n):
            clauses.append([var[i]])
            for j in range(i+1, n):
                clauses.append([f'~{var[i]}', f'~{var[j]}', var[j-i-1]])
                clauses.append([f'{var[i]}', f'{var[j]}', f'~{var[j-i-1]}'])
        return clauses
    
    def tseitin_to_polynomial(clauses):
        # Convert Tseitin formula to polynomial
        n = len(clauses)
        poly = [0] * (2**n)
        for clause in clauses:
            if len(clause) == 1:
                var_index = int(clause[0][1:]) - 1
                poly[1 << var_index] += 1
            else:
                term = 1
                for lit in clause:
                    if lit.startswith('~'):
                        var_index = int(lit[1:]) - 1
                        term *= (1 - (1 << var_index))
                    else:
                        var_index = int(lit) - 1
                        term *= (1 + (1 << var_index))
                poly[term] += 1
        return poly
    
    def find_roots(poly):
        # Find distinct roots of the polynomial
        n = len(poly)
        roots = set()
        for i in range(n):
            if poly[i] != 0:
                root = Fraction(i, 2**n)
                roots.add(root)
        return roots
    
    def resolution_width(clauses):
        # Compute resolution proof width
        stack = []
        visited = set()
        for clause in clauses:
            stack.append(clause)
            visited.add(tuple(sorted(clause)))
        
        while stack:
            clause1 = stack.pop()
            if len(clause1) == 1:
                return len(visited)
            
            lit = clause1[0]
            if lit.startswith('~'):
                other_lit = f'{lit[1]}'
            else:
                other_lit = f'~{lit}'
            
            for clause2 in clauses:
                if other_lit in clause2:
                    new_clause = [l for l in clause2 if l != other_lit]
                    if len(new_clause) == 0:
                        return len(visited)
                    stack.append(sorted(new_clause))
                    visited.add(tuple(sorted(new_clause)))
        
        return len(visited)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        clauses = generate_tseitin_formula(n)
        poly = tseitin_to_polynomial(clauses)
        roots = find_roots(poly)
        width = resolution_width(clauses)
        
        results.append({
            "n": n,
            "roots": len(roots),
            "width": width
        })
    
    if not results:
        return {
            "metric_name": "resolution_width",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_max = max(r["n"] for r in results)
    instances_tested = len(results)
    roots_values = [r["roots"] for r in results]
    width_values = [r["width"] for r in results]
    
    mean_roots = sum(roots_values) / instances_tested
    mean_width = sum(width_values) / instances_tested
    
    correlation_coefficient = 0.0
    if len(results) > 1:
        numerator = sum((roots_values[i] - mean_roots) * (width_values[i] - mean_width) for i in range(instances_tested))
        denominator = math.sqrt(sum((roots_values[i] - mean_roots)**2 * (width_values[i] - mean_width)**2 for i in range(instances_tested)))
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "resolution_width",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8 and all(corr > 0.5 for corr in [r["roots"] / r["width"] for r in results]),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) if sys.argv[1:] else [2**i + 1 for i in range(5, 30)]
    
    trials = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{trial_result}...}}")
        trials.append(trial_result)
    
    mean_metric_value = sum(t["metric_value"] for t in trials) / len(trials)
    std_metric_value = math.sqrt(sum((t["metric_value"] - mean_metric_value)**2 for t in trials) / len(trials))
    support_fraction = sum(1 for t in trials if t["conjecture_holds"]) / len(trials)
    
    if all(t["conjecture_holds"] for t in trials):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(t["metric_value"] <= 0.5 for t in trials):
        first_failing_seed = next(seed for seed, trial in zip(seeds, trials) if not trial["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")