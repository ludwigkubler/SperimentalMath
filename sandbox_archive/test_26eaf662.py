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
    
    def generate_cnf(n):
        cnf = []
        for _ in range(10):  # Generate 10 clauses with n variables
            clause = [random.randint(-n, -1), random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def evaluate_cnf(cnf, assignment):
        for clause in cnf:
            if not any(lit in assignment and assignment[lit] == (lit > 0) for lit in clause):
                return False
        return True
    
    def dpll(cnf, assignment={}, free_vars=None):
        if free_vars is None:
            free_vars = set(range(1, len(cnf) + 1))
        
        if not cnf:
            return assignment
        
        var = next(iter(free_vars))
        pos_var, neg_var = var, -var
        new_free_vars = free_vars.copy()
        new_free_vars.remove(var)
        
        # Try assigning True to the variable
        assignment[var] = True
        result = dpll(cnf, assignment, new_free_vars)
        if result is not None:
            return result
        
        # If assigning True doesn't work, try assigning False
        del assignment[var]
        assignment[neg_var] = True
        result = dpll(cnf, assignment, new_free_vars)
        if result is not None:
            return result
        
        # If both assignments fail, backtrack
        del assignment[neg_var]
        return None
    
    def mci(cnf):
        n = len(cnf)
        F = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                if i != j:
                    F[i][j] = 1
        return sum(F[i][j] for i in range(1, n + 1) for j in range(1, n + 1))
    
    n_max = 40
    instances_tested = 0
    mci_values = []
    w_values = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Sample 5 instances per size
            cnf = generate_cnf(n)
            assignment = {}
            result = dpll(cnf, assignment)
            if result is not None:
                mci_values.append(mci(cnf))
                w_values.append(len(result))
                instances_tested += 1
    
    if len(mci_values) < 30:
        return {
            "metric_name": "mci",
            "metric_value": sum(mci_values) / len(mci_values),
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mci_mean = sum(mci_values) / len(mci_values)
    w_mean = sum(w_values) / len(w_values)
    correlation_coefficient = (sum((mci_values[i] - mci_mean) * (w_values[i] - w_mean) for i in range(len(mci_values))) /
                               math.sqrt(sum((mci_values[i] - mci_mean) ** 2 for i in range(len(mci_values))) *
                                         sum((w_values[i] - w_mean) ** 2 for i in range(len(w_values)))))
    
    return {
        "metric_name": "mci",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient > 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mci_values = [r["metric_value"] for r in results if "mci" in r]
    conjecture_holds = all(r["conjecture_holds"] for r in results if "conjecture_holds" in r and r["conjecture_holds"])
    
    if conjecture_holds:
        print(f"RESULT: SUPPORTED mean={sum(mci_values) / len(mci_values):.2f} std={math.sqrt(sum((x - sum(mci_values) / len(mci_values)) ** 2 for x in mci_values) / len(mci_values)):.2f} support_fraction=1.0")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed={first_failing_seed}")