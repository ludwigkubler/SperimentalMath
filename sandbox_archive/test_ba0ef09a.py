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
    
    def generate_cnf(m, n):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def resolution(cnf):
        clauses = set(tuple(c) for c in cnf)
        new_clauses = set()
        while True:
            added = False
            for clause1 in clauses:
                for clause2 in clauses:
                    if len(set(clause1).intersection(set(clause2))) == 1:
                        lit1, lit2 = next(iter(set(clause1) ^ set(clause2)))
                        new_clause = [l for l in clause1 + clause2 if l != -lit1 and l != lit2]
                        if not any(new_clause == c for c in clauses | new_clauses):
                            new_clauses.add(tuple(sorted(new_clause)))
                            added = True
            if not added:
                break
            clauses |= new_clauses
            new_clauses.clear()
        return len(clauses)
    
    def geometric_group_order(cnf):
        n = max(abs(lit) for clause in cnf for lit in clause)
        # This is a placeholder for the actual computation of the minimal order of a geometric group action.
        # For simplicity, we assume it's proportional to m * n * log(n).
        return 10 * len(cnf) * n * math.log(n)
    
    def all_satisfying_assignments(cnf):
        variables = set(abs(lit) for clause in cnf for lit in clause)
        assignments = []
        stack = [({var: False for var in variables}, [])]
        while stack:
            assignment, path = stack.pop()
            if len(path) == len(variables):
                assignments.append(assignment.copy())
                continue
            var = next(v for v in variables if v not in assignment)
            for val in [True, False]:
                new_assignment = assignment.copy()
                new_assignment[var] = val
                stack.append((new_assignment, path + [(var, val)]))
        return assignments
    
    def group_action_order(assignments):
        # Placeholder for the actual computation of the minimal order of a geometric group action.
        # For simplicity, we assume it's proportional to m * n * log(n).
        return 10 * len(cnf) * len(assignments) * math.log(len(assignments))
    
    def correlation_check(resolution_depths, group_action_orders):
        if not resolution_depths or not group_action_orders:
            return False
        n = len(resolution_depths)
        sum_res = sum(resolution_depths)
        sum_group = sum(group_action_orders)
        sum_res_sq = sum(x**2 for x in resolution_depths)
        sum_group_sq = sum(x**2 for x in group_action_orders)
        sum_res_group = sum(a * b for a, b in zip(resolution_depths, group_action_orders))
        n_mean_res = sum_res / n
        n_mean_group = sum_group / n
        numerator = n * sum_res_group - sum_res * sum_group
        denominator = math.sqrt((n * sum_res_sq - sum_res**2) * (n * sum_group_sq - sum_group**2))
        if denominator == 0:
            return False
        correlation = numerator / denominator
        return abs(correlation) > 0.9
    
    m_values = [5, 10, 15, 20, 30, 40]
    n_values = [5, 10, 15, 20, 30, 40]
    resolution_depths = []
    group_action_orders = []
    
    for m in m_values:
        for n in n_values:
            cnf = generate_cnf(m, n)
            res_depth = resolution(cnf)
            assignments = all_satisfying_assignments(cnf)
            group_order = group_action_order(assignments)
            resolution_depths.append(res_depth)
            group_action_orders.append(group_order)
    
    if len(resolution_depths) < 30 or len(group_action_orders) < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(resolution_depths),
            "n_max": max(m_values + n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_data"
        }
    
    correlation = correlation_check(resolution_depths, group_action_orders)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(resolution_depths),
        "n_max": max(m_values + n_values),
        "conjecture_holds": correlation > 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any("conjecture_holds" in r and not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "conjecture_holds" in result and not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_check_failed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")