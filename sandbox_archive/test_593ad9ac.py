# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def tseytin_transformation(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        
        # Create literals
        literals = [random.choice([var, f'{var}']) for var in variables]
        
        # Create Tseytin transformation
        for i in range(n):
            if literals[i] == variables[i]:
                clauses.append([f'x{i+1}', f'y{i+1}', f'-z{i+1}'])
                clauses.append([f'-x{i+1}', f'-y{i+1}', f'z{i+1}'])
                clauses.append([f'-x{i+1}', f'y{i+1}', f'-z{i+1}'])
                clauses.append([f'x{i+1}', f'-y{i+1}', f'z{i+1}'])
            else:
                clauses.append([f'x{i+1}', f'-y{i+1}', f'-z{i+1}'])
                clauses.append([f'-x{i+1}', f'y{i+1}', f'z{i+1}'])
                clauses.append([f'-x{i+1}', f'-y{i+1}', f'z{i+1}'])
                clauses.append([f'x{i+1}', f'y{i+1}', f'-z{i+1}'])
        
        # Create final clause
        for i in range(n):
            if literals[i] == variables[i]:
                clauses.append([f'-y{i+1}', f'-z{i+1}'])
            else:
                clauses.append([f'y{i+1}', f'z{i+1}'])
        
        return literals, clauses
    
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            if literal.startswith('-'):
                if literal[1:] in assignment and assignment[literal[1:]]:
                    return False
                else:
                    assignment[literal[1:]] = True
            else:
                if literal in assignment and not assignment[literal]:
                    return False
                else:
                    assignment[literal] = True
            new_clauses = [c for c in clauses if literal not in c]
            new_clauses = [[l for l in c if l != literal and l != f'-{literal}'] for c in new_clauses]
            return dpll(new_clauses, assignment)
        pure_literal = next((l for l in variables if all(l in c or f'-{l}' in c for c in clauses)), None)
        if pure_literal:
            if pure_literal.startswith('-'):
                assignment[pure_literal[1:]] = False
            else:
                assignment[pure_literal] = True
            new_clauses = [c for c in clauses if pure_literal not in c]
            new_clauses = [[l for l in c if l != pure_literal and l != f'-{pure_literal}'] for c in new_clauses]
            return dpll(new_clauses, assignment)
        p = random.choice(variables)
        assignment[p] = True
        new_clauses = [c for c in clauses if p not in c]
        new_clauses = [[l for l in c if l != p and l != f'-{p}'] for c in new_clauses]
        if dpll(new_clauses, assignment):
            return True
        assignment[p] = False
        new_clauses = [c for c in clauses if p not in c]
        new_clauses = [[l for l in c if l != p and l != f'-{p}'] for c in new_clauses]
        return dpll(new_clauses, assignment)
    
    def geometric_measure(n):
        grid_size = 10
        area = 0
        for i in range(grid_size):
            for j in range(grid_size):
                if (i + j) % n == 0:
                    area += 1
        return Fraction(area * grid_size * grid_size, n * n)
    
    def dpll_path_length(clauses):
        assignment = {}
        return len(dpll(clauses, assignment))
    
    n_values = [5, 10, 15, 20, 30, 40]
    metrics = []
    for n in n_values:
        literals, clauses = tseytin_transformation(n)
        mgm = geometric_measure(n)
        l = dpll_path_length(clauses)
        metrics.append({"n": n, "mgm": mgm, "l": l})
    
    correlation_coefficient = sum((metrics[i]["mgm"] - sum(m["mgm"] for m in metrics) / len(metrics)) * (metrics[i]["l"] - sum(m["l"] for m in metrics) / len(metrics)) for i in range(len(metrics))) / (len(metrics) * sum((metrics[i]["mgm"] - sum(m["mgm"] for m in metrics) / len(metrics)) ** 2 for i in range(len(metrics))) * sum((metrics[i]["l"] - sum(m["l"] for m in metrics) / len(metrics)) ** 2 for i in range(len(metrics)))) ** 0.5
    p_value = 2 * (1 - 0.5 ** len(metrics))
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(m["n"] for m in metrics),
        "conjecture_holds": correlation_coefficient >= 0.8 and p_value <= 0.05,
        "counterexample": "" if correlation_coefficient >= 0.8 and p_value <= 0.05 else f"Correlation: {correlation_coefficient}, P-value: {p_value}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and sum(1 for r in results if not r["conjecture_holds"]) / len(results) <= 0.2:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")