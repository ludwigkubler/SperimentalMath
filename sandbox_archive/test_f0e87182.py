# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n - 1):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[j] for i, j in combinations(range(n), 2)):
                clauses.append(clause)
        return clauses
    
    def dpll(cnf):
        def dpll_helper(model, clause_index):
            if clause_index == len(cnf):
                return True
            literals = cnf[clause_index]
            for literal in literals:
                new_model = model.copy()
                if literal > 0:
                    new_model.add(literal)
                else:
                    new_model.discard(-literal)
                if dpll_helper(new_model, clause_index + 1):
                    return True
            return False
        
        return dpll_helper(set(), 0)
    
    def arithmetic_hierarchy_depth(cnf):
        depth = 0
        for clause in cnf:
            depth = max(depth, len(clause))
        return depth
    
    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n)
            depth = arithmetic_hierarchy_depth(cnf)
            path_length = dpll(cnf)
            if path_length > 0:
                metric_values.append(Fraction(depth, path_length))
    
    if not metric_values:
        return {
            "metric_name": "Arithmetic Hierarchy Depth / DPLL Proof Path Length",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    mean_value = sum(metric_values) / len(metric_values)
    std_dev = (sum((x - mean_value)**2 for x in metric_values) / len(metric_values))**0.5
    
    return {
        "metric_name": "Arithmetic Hierarchy Depth / DPLL Proof Path Length",
        "metric_value": float(mean_value),
        "instances_tested": len(metric_values),
        "n_max": max(n_values),
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev = (sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={r['seed']}")
                break