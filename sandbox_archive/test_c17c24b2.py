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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[j] for j in range(i)):
                clauses.append(clause)
        return clauses
    
    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        unit_clauses = [c[0] for c in cnf if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
                return True
            else:
                return False
        pure_literals = set()
        for literal in range(1, n + 1):
            pos_count = sum(1 for clause in cnf if literal in clause)
            neg_count = sum(1 for clause in cnf if -literal in clause)
            if pos_count == 0:
                pure_literals.add(-literal)
            elif neg_count == 0:
                pure_literals.add(literal)
        if pure_literals:
            literal = pure_literals.pop()
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
                return True
            else:
                return False
        unassigned_literal = next(l for l in range(1, n + 1) if l not in assignment)
        new_assignment_true = assignment.copy()
        new_assignment_true[unassigned_literal] = True
        if dpll(cnf, new_assignment_true):
            return True
        new_assignment_false = assignment.copy()
        new_assignment_false[unassigned_literal] = False
        if dpll(cnf, new_assignment_false):
            return True
        else:
            return False
    
    def geometric_entropy(n):
        # Placeholder for actual geometric entropy computation
        # This is a dummy implementation that returns a random value
        return random.random()
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        cnf = generate_cnf(n)
        mge_value = geometric_entropy(n)
        path_length = dpll(cnf)
        results.append((mge_value, path_length))
    
    if len(results) < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mge_values = [r[0] for r in results]
    path_lengths = [r[1] for r in results]
    mean_mge = sum(mge_values) / len(mge_values)
    mean_path_length = sum(path_lengths) / len(path_lengths)
    covariance = sum((m - mean_mge) * (p - mean_path_length) for m, p in results) / len(results)
    variance_mge = sum((m - mean_mge) ** 2 for m in mge_values) / len(mge_values)
    variance_path_length = sum((p - mean_path_length) ** 2 for p in path_lengths) / len(path_lengths)
    correlation_coefficient = covariance / (math.sqrt(variance_mge) * math.sqrt(variance_path_length))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print("RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed=<s>")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")