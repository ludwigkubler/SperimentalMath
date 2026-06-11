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
    
    def generate_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            while len(set(clause)) != 2:
                clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses

    def dpll_tree_height(clauses):
        if not clauses:
            return 0
        literals = set()
        for clause in clauses:
            literals.update(abs(lit) for lit in clause)
        assignment = {lit: None for lit in literals}
        
        def backtrack(current_clauses, current_assignment):
            if not current_clauses:
                return 0
            unit_clause = next((c for c in current_clauses if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                new_assignment = current_assignment.copy()
                new_assignment[literal] = True
                new_assignment[-literal] = False
                return backtrack([c for c in current_clauses if literal not in c and -literal not in c], new_assignment) + 1
            
            pure_literal = next((lit for lit in literals if (all(lit in c or -lit in c for c in current_clauses)) and (-lit in literals)), None)
            if pure_literal:
                new_assignment = current_assignment.copy()
                new_assignment[pure_literal] = True
                new_assignment[-pure_literal] = False
                return backtrack([c for c in current_clauses if pure_literal not in c and -pure_literal not in c], new_assignment) + 1
            
            literal, _ = random.choice(list(current_clauses[0]))
            new_assignment = current_assignment.copy()
            new_assignment[literal] = True
            new_assignment[-literal] = False
            return backtrack([c for c in current_clauses if literal not in c and -literal not in c], new_assignment) + 1
        
        return backtrack(clauses, assignment)
    
    def minimal_formal_context_width(clauses):
        variables = set(abs(lit) for clause in clauses for lit in clause)
        context = {var: [] for var in variables}
        
        for clause in clauses:
            for i, var in enumerate(variables):
                if var in clause:
                    context[var].append(i)
        
        width = 0
        for var in variables:
            width = max(width, len(context[var]))
        
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            clauses = generate_cnf(n, int(1.5 * n))
            mfw = minimal_formal_context_width(clauses)
            w = dpll_tree_height(clauses)
            results.append((mfw, w))
    
    if not results:
        return {
            "metric_name": "Pearson Correlation Coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    mfw_values = [mfw for mfw, _ in results]
    w_values = [w for _, w in results]
    
    mean_mfw = sum(mfw_values) / len(mfw_values)
    mean_w = sum(w_values) / len(w_values)
    
    covariance = sum((mfw - mean_mfw) * (w - mean_w) for mfw, w in results) / len(results)
    variance_mfw = sum((mfw - mean_mfw) ** 2 for mfw in mfw_values) / len(mfw_values)
    variance_w = sum((w - mean_w) ** 2 for w in w_values) / len(w_values)
    
    pearson_corr_coeff = covariance / (math.sqrt(variance_mfw) * math.sqrt(variance_w))
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": pearson_corr_coeff,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(pearson_corr_coeff) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
    
    results = [run_trial(seed) for seed in seeds]
    mean_corr_coeff = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for result in results if abs(result["metric_value"]) >= 0.8) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=NA support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Pearson correlation coefficient does not meet threshold\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")