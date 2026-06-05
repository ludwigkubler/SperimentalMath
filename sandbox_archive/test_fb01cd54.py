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

def generate_formula(n):
    variables = list(range(1, n + 1))
    clauses = []
    
    for _ in range(n):
        clause = [random.choice([1, -1]) * var for var in variables]
        if all(clause[i] != -clause[j] for j in range(i)):
            clauses.append(clause)
    
    return clauses

def dpll(clauses, assignment):
    unsatisfied = [c for c in clauses if not any(lit == 0 for lit in c)]
    if not unsatisfied:
        return True
    unit_clauses = [c for c in unsatisfied if len(c) == 1]
    if unit_clauses:
        literal = unit_clauses[0][0]
        assignment[abs(literal)] = literal > 0
        return dpll(clauses, assignment)
    
    var = next(var for var in range(1, len(assignment) + 1) if var not in assignment)
    assignment[var] = True
    if dpll(clauses, assignment):
        return True
    assignment[var] = False
    return dpll(clauses, assignment)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    m_n = []
    w_n = []
    
    for n in n_values:
        clauses = generate_formula(n)
        assignment = {}
        
        if dpll(clauses, assignment):
            depth = len(assignment) - sum(1 for var, val in assignment.items() if val is False)
            m_n.append(len(set(tuple(sorted(c)) for c in clauses)))
            w_n.append(depth)
    
    if not m_n or not w_n:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_m_n = sum(m_n) / len(m_n)
    mean_w_n = sum(w_n) / len(w_n)
    
    numerator = sum((m - mean_m_n) * (w - mean_w_n) for m, w in zip(m_n, w_n))
    denominator = math.sqrt(sum((m - mean_m_n) ** 2 for m in m_n)) * math.sqrt(sum((w - mean_w_n) ** 2 for w in w_n))
    
    if denominator == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(m_n),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    pearson_corr = numerator / denominator
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": len(m_n),
        "n_max": max(n_values),
        "conjecture_holds": pearson_corr >= 0.8 and p_value <= 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")