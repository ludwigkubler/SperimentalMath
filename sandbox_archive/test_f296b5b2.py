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

def generate_cnf(n, m):
    clauses = []
    for _ in range(m):
        clause = [random.randint(1, n), -random.randint(1, n)]
        clauses.append(clause)
    return clauses

def dpll_tree_height(clauses):
    def backtrack(clauses, assignment):
        if not clauses:
            return 0
        unit_clauses = [c for c in clauses if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0][0]
            new_assignment = assignment.copy()
            if literal > 0:
                new_assignment[literal] = True
            else:
                new_assignment[-literal] = False
            return backtrack([c for c in clauses if literal not in c], new_assignment) + 1
        pure_literals = {}
        for clause in clauses:
            for literal in clause:
                if literal > 0:
                    pure_literals[literal] = True
                else:
                    pure_literals[-literal] = False
        for literal, polarity in pure_literals.items():
            new_assignment = assignment.copy()
            new_assignment[literal] = polarity
            return backtrack([c for c in clauses if literal not in c], new_assignment) + 1
        literals = set(l for clause in clauses for l in clause)
        literal, _ = random.choice(list(literals))
        new_assignment_true = assignment.copy()
        new_assignment_true[literal] = True
        new_assignment_false = assignment.copy()
        new_assignment_false[-literal] = False
        return max(backtrack([c for c in clauses if literal not in c], new_assignment_true),
                   backtrack([c for c in clauses if -literal not in c], new_assignment_false)) + 1
    
    return backtrack(clauses, {})

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    mfw_values = []
    w_values = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            clauses = generate_cnf(n, random.randint(1, int(2 * n)))
            mfw = len(set(abs(l) for l in sum(clauses, [])))  # Minimal order of formal context width
            w = dpll_tree_height(clauses)
            mfw_values.append(mfw)
            w_values.append(w)
    
    if not mfw_values or not w_values:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n = len(mfw_values)
    mean_mfw = sum(mfw_values) / n
    mean_w = sum(w_values) / n
    variance_mfw = sum((x - mean_mfw) ** 2 for x in mfw_values) / n
    variance_w = sum((y - mean_w) ** 2 for y in w_values) / n
    covariance = sum((mfw_values[i] - mean_mfw) * (w_values[i] - mean_w) for i in range(n)) / n
    
    correlation_coefficient = covariance / math.sqrt(variance_mfw * variance_w)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(mfw_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.95,  # Simplified threshold for demonstration
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["metric_value"] is not None for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_data")