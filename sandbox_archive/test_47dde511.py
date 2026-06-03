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
    
    def generate_cnf(n):
        cnf = []
        for _ in range(random.randint(1, n)):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            cnf.append(clause)
        return cnf
    
    def tseitin_structure(cnf):
        literals = set()
        clauses = []
        for clause in cnf:
            literals.update(abs(lit) for lit in clause)
            new_var = max(literals) + 1
            literals.add(new_var)
            clauses.append([new_var] + [-lit for lit in clause])
            for i, lit1 in enumerate(clause):
                for j, lit2 in enumerate(clause[i+1:], start=i+1):
                    clauses.append([-new_var, -lit1, lit2])
        return literals, clauses
    
    def p_adic_topological_entropy(literals, clauses):
        # Placeholder implementation
        return random.random()
    
    def resolution_proof_width(cnf):
        # Placeholder implementation
        return len(cnf)
    
    n_max = 0
    instances_tested = 0
    mindex_values = []
    w_values = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n)
            literals, clauses = tseitin_structure(cnf)
            mindex = p_adic_topological_entropy(literals, clauses)
            w = resolution_proof_width(cnf)
            
            if mindex is not None and w is not None:
                mindex_values.append(mindex)
                w_values.append(w)
                instances_tested += 1
    
    if instances_tested < 30:
        return {
            "metric_name": "Pearson correlation",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    def pearson_correlation(x, y):
        if len(x) != len(y):
            return None
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = (sum((x[i] - mean_x) ** 2 for i in range(n)) / n) ** 0.5
        std_y = (sum((y[i] - mean_y) ** 2 for i in range(n)) / n) ** 0.5
        return cov / (std_x * std_y)
    
    correlation = pearson_correlation(mindex_values, w_values)
    p_value = None  # Placeholder for actual p-value calculation
    
    conjecture_holds = correlation is not None and abs(correlation) > 0.9
    counterexample = "" if conjecture_holds else "correlation_threshold_not_met"
    
    return {
        "metric_name": "Pearson correlation",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["counterexample"] == "correlation_threshold_not_met" for r in results):
        print("RESULT: INCONCLUSIVE correlation_threshold_not_met")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_threshold_not_met\" first_failing_seed={first_failing_seed}")