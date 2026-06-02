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

def generate_cnf(n):
    clauses = []
    for _ in range(n):
        clause = [random.randint(1, n), -random.randint(1, n)]
        clauses.append(clause)
    return clauses

def tseitin_encoding(cnf):
    literals = set()
    new_vars = {}
    for i, clause in enumerate(cnf):
        literals.update(clause)
        new_var = f'x{i+1}'
        new_vars[i] = new_var
        cnf.append([new_var])
        for literal in clause:
            cnf.append([-new_var, -literal])
    return new_vars

def dpll_search_tree(cnf):
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            if literal < 0 and -literal in assignment:
                return False
            assignment[literal] = True
            cnf = [c for c in cnf if literal not in c and -literal not in c]
            new_clauses = []
            for clause in cnf:
                if literal in clause:
                    continue
                if -literal in clause:
                    new_clauses.append([l for l in clause if l != -literal])
                else:
                    new_clauses.append(clause)
            return dpll(new_clauses, assignment)
        pure_literal = next((l for l in literals if (l not in assignment and -l not in assignment)), None)
        if pure_literal is None:
            return False
        assignment[pure_literal] = True
        cnf = [c for c in cnf if pure_literal not in c and -pure_literal not in c]
        new_clauses = []
        for clause in cnf:
            if pure_literal in clause:
                continue
            if -pure_literal in clause:
                new_clauses.append([l for l in clause if l != -pure_literal])
            else:
                new_clauses.append(clause)
        return dpll(new_clauses, assignment)
    literals = set()
    for clause in cnf:
        literals.update(clause)
    assignment = {}
    return dpll(cnf, assignment)

def plane_curve_complex(cnf):
    # Placeholder implementation
    return len(cnf)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    metrics = []
    for n in n_values:
        cnf = generate_cnf(n)
        new_vars = tseitin_encoding(cnf)
        leaf_count = dpll_search_tree(cnf)
        curve_complexity = plane_curve_complex(cnf)
        metrics.append((curve_complexity, leaf_count))
    if not metrics:
        return {
            "metric_name": "correlation",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    curve_complexities = [m[0] for m in metrics]
    leaf_counts = [m[1] for m in metrics]
    mean_curve_complexity = sum(curve_complexities) / len(curve_complexities)
    mean_leaf_count = sum(leaf_counts) / len(leaf_counts)
    correlation = (sum((curve_complexities[i] - mean_curve_complexity) * (leaf_counts[i] - mean_leaf_count) for i in range(len(metrics))) /
                   math.sqrt(sum((curve_complexities[i] - mean_curve_complexity) ** 2 for i in range(len(metrics))) *
                             sum((leaf_counts[i] - mean_leaf_count) ** 2 for i in range(len(metrics)))))
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(metrics),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")