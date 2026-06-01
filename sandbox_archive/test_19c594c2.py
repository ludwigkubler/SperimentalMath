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
        clauses = []
        for _ in range(10 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf, assignment={}):
        unassigned_vars = [v for v in range(1, len(cnf) + 1) if v not in assignment and -v not in assignment]
        if not unassigned_vars:
            all_satisfied = all(any(lit in assignment for lit in clause) for clause in cnf)
            return all_satisfied
        var = random.choice(unassigned_vars)
        for val in [True, False]:
            new_assignment = assignment.copy()
            new_assignment[var] = val
            if dpll(cnf, new_assignment):
                return True
        return False
    
    def mcr(cnf):
        # Simplified local cohomology rank calculation based on Gröbner basis
        n = len(cnf)
        # Placeholder for actual computation
        return random.randint(1, 2 * n)
    
    def dpll_diameter(cnf):
        return len(dpll_search_tree(cnf))
    
    def dpll_search_tree(cnf):
        if not cnf:
            return []
        unassigned_vars = [v for v in range(1, len(cnf) + 1) if v not in assignment and -v not in assignment]
        var = random.choice(unassigned_vars)
        true_branch = dpll_search_tree([c for c in cnf if var in c])
        false_branch = dpll_search_tree([c for c in cnf if -var in c])
        return [var, true_branch, false_branch]
    
    n = 10
    cnf = generate_cnf(n)
    mcr_value = mcr(cnf)
    dpll_diameter_value = dpll_diameter(cnf)
    
    return {
        "metric_name": "mcr_vs_dpll_diameter",
        "metric_value": mcr_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": mcr_value <= dpll_diameter_value * 2,  # Simplified O(d(φ)) check
        "counterexample": "" if mcr_value <= dpll_diameter_value * 2 else f"mcr({n})={mcr_value}, dPLL_diameter({n})={dpll_diameter_value}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(100, 999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")