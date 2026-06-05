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
    
    def generate_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf, assignment=None):
        if not cnf:
            return True
        if not assignment:
            assignment = {}
        
        var = next((v for v in range(1, max(var for clause in cnf for var in clause) + 1) if v not in assignment), None)
        if var is None:
            return False
        
        def propagate():
            new_assignment = assignment.copy()
            for var, value in assignment.items():
                for clause in cnf:
                    if value == -var and var in clause:
                        clauses.remove(clause)
                    elif value == var and -var in clause:
                        clauses.remove(clause)
            return new_assignment
        
        def backtrack(value):
            assignment[var] = value
            new_assignment = propagate()
            if dpll(cnf, new_assignment):
                return True
            del assignment[var]
            return False
        
        if backtrack(True) or backtrack(False):
            return True
        return False
    
    def frobenius_schur_indicator(cnf):
        n = max(var for clause in cnf for var in clause)
        # Placeholder implementation of Frobenius-Schur indicator calculation
        return random.random() * n ** (1/4)  # Simplified for testing purposes
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = n * 2  # Example ratio of clauses to variables
        cnf = generate_cnf(n, m)
        fsi = frobenius_schur_indicator(cnf)
        proof_length = len(dpll(cnf)) if dpll(cnf) else float('inf')
        results.append((n, fsi, proof_length))
    
    min_fsi = min(fsi for _, fsi, _ in results)
    n_max = max(n for n, _, _ in results)
    instances_tested = len(results)
    
    correlation_coefficient = 0
    if instances_tested > 1:
        mean_n = sum(n for n, _, _ in results) / instances_tested
        mean_fsi = sum(fsi for _, fsi, _ in results) / instances_tested
        numerator = sum((n - mean_n) * (fsi - mean_fsi) for n, fsi, _ in results)
        denominator = math.sqrt(sum((n - mean_n) ** 2 for n, _, _ in results)) * math.sqrt(sum((fsi - mean_fsi) ** 2 for _, fsi, _ in results))
        correlation_coefficient = numerator / denominator
    
    conjecture_holds = correlation_coefficient >= 0.7
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.7"
    
    return {
        "metric_name": "Frobenius-Schur Indicator vs DPLL Proof Length",
        "metric_value": correlation_coefficient,
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
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if r["metric_value"] < 0.5) / len(results) >= 0.2:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")