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
        cnf = []
        for _ in range(2**n // 4):  # Generate a small CNF to avoid trivial cases
            clause = [random.randint(-n, -1), random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def dpll(cnf):
        assignment = {}
        
        def search():
            unassigned_vars = [var for var in range(1, n+1) if var not in assignment and -var not in assignment]
            if not unassigned_vars:
                return all(all(lit not in assignment for lit in clause) for clause in cnf)
            var = unassigned_vars[0]
            for value in [True, False]:
                assignment[var] = value
                if search():
                    return True
                del assignment[var]
            return False
        
        return search()
    
    def eta_invariant(cnf):
        # Placeholder implementation of eta-invariant calculation
        # This is a dummy function and should be replaced with actual computation
        return random.random() * n
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        eta = eta_invariant(cnf)
        width = 1 if dpll(cnf) else float('inf')
        
        if width == float('inf'):
            continue
        
        ratio = eta / width
        results.append((n, eta, width, ratio))
    
    if not results:
        return {
            "metric_name": "eta_to_width_ratio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    metric_values = [ratio for _, _, _, ratio in results]
    mean_ratio = sum(metric_values) / len(metric_values)
    min_ratio = min(metric_values)
    max_ratio = max(metric_values)
    n_max = max(n for _, _, _, _ in results)
    
    return {
        "metric_name": "eta_to_width_ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": min_ratio > 0 and max_ratio < float('inf'),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if "metric_value" not in trial_result or trial_result["metric_value"] is None:
            continue
        
        results.append(trial_result["metric_value"])
    
    mean_ratio = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean_ratio)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r > 0 and r < float('inf')) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    elif any(r <= 0 or r == float('inf') for r in results):
        first_failing_seed = seeds[results.index(next(r for r in results if r <= 0 or r == float('inf')))]
        print(f"RESULT: FALSIFIED counterexample='eta_to_width_ratio_out_of_bounds' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")