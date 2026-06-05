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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def dpll(cnf):
        def backtrack(assignment):
            unassigned_vars = [var for var in range(1, n+1) if var not in assignment]
            if not unassigned_vars:
                return all([any([assignment[var] for var in clause]) for clause in cnf])
            var = unassigned_vars[0]
            for val in [True, False]:
                new_assignment = assignment.copy()
                new_assignment[var] = val
                if backtrack(new_assignment):
                    return True
            return False
        
        assignment = {}
        return backtrack(assignment)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = random.randint(n, 2*n)  # Ensure at least one clause per variable
        cnf = generate_cnf(n, m)
        proof_length = len(dpll(cnf)) if dpll(cnf) else float('inf')
        min_FSI = n ** (1/4)
        results.append((min_FSI, proof_length))
    
    metric_value = sum(proof_length for _, proof_length in results) / len(results)
    instances_tested = len(results)
    n_max = max(n_values)
    conjecture_holds = all(0.5 <= proof_length / min_FSI <= 2.0 for min_FSI, proof_length in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "DPLL Proof Length",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        print("RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed=<s>")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction")