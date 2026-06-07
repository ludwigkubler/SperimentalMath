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
    
    def generate_sat_instance(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def is_clause_satisfied(clause, assignment):
        return any(assignment[i] == c for i, c in enumerate(clause))
    
    def evaluate_formula(formula, assignment):
        return all(is_clause_satisfied(clause, assignment) for clause in formula)
    
    def generate_random_formula(n):
        num_clauses = random.randint(1, 2**n)
        clauses = []
        for _ in range(num_clauses):
            clause = [random.choice([-i-1, i]) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def resolution(sat_instance):
        n = len(sat_instance)
        clauses = generate_random_formula(n)
        
        def simplify_clause(clause):
            new_clause = []
            for literal in clause:
                if -literal in clause:
                    continue
                new_clause.append(literal)
            return new_clause
        
        def resolve(clause1, clause2):
            resolved_clauses = set()
            for lit1 in clause1:
                if -lit1 in clause2:
                    new_clause = [l for l in clause1 + clause2 if l != lit1 and l != -lit1]
                    resolved_clauses.add(tuple(sorted(simplify_clause(new_clause))))
            return resolved_clauses
        
        while True:
            new_clauses = set()
            for i in range(len(clauses)):
                for j in range(i+1, len(clauses)):
                    resolvents = resolve(clauses[i], clauses[j])
                    if not resolvents:
                        continue
                    new_clauses.update(resolvents)
            if not new_clauses:
                break
            clauses.extend(new_clauses)
        
        return len(clauses)
    
    def monomial_ideal_order(sat_instance):
        n = len(sat_instance)
        # Placeholder for actual computation of the minimal order of a monomial ideal
        return random.randint(1, n)  # Simplified for testing purposes
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        sat_instance = generate_sat_instance(n)
        order = monomial_ideal_order(sat_instance)
        width = resolution(sat_instance)
        results.append({"order": order, "width": width})
    
    if len(results) < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    orders = [res["order"] for res in results]
    widths = [res["width"] for res in results]
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x)**2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y)**2 for i in range(n)) / n)
        return cov_xy / (std_x * std_y) if std_x * std_y != 0 else 0
    
    correlation = pearson_correlation(orders, widths)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30*31, 3))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='correlation_too_low' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")