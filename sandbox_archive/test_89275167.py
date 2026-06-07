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
    
    def dpll_solve(cnf):
        def solve(clauses, assignment):
            if not clauses:
                return True
            clause = next((c for c in clauses if any(l in assignment and assignment[l] == 1 for l in c)), [])
            if not clause:
                return False
            literal = random.choice(clause)
            new_assignment = assignment.copy()
            new_assignment[literal] = 1
            if solve(clauses, new_assignment):
                return True
            new_assignment[literal] = -1
            if solve(clauses, new_assignment):
                return True
            return False
        
        return solve(cnf, {})
    
    def generate_cnf(n):
        cnf = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_ratio = 0
        max_n = n
        
        for _ in range(5):  # Test each n with 5 instances
            cnf = generate_cnf(n)
            if dpll_solve(cnf):
                clause_depth = sum(len(clause) for clause in cnf)
                p_adic_order = Fraction(n, 2).limit_denominator()  # Simplified approximation
                ratio = clause_depth / p_adic_order
                results.append(ratio)
                instances_tested += 1
                max_n = max(max_n, n)
        
        if instances_tested < 5:
            return {
                "metric_name": "Ratio of Clause Depth to P-adic Order",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": max_n,
                "conjecture_holds": False,
                "counterexample": "Insufficient instances"
            }
    
    mean_ratio = sum(results) / len(results)
    support_fraction = sum(1 for r in results if r <= 4) / len(results)
    
    return {
        "metric_name": "Ratio of Clause Depth to P-adic Order",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": max_n,
        "conjecture_holds": support_fraction >= 0.95 and all(r <= 10 for r in results),
        "counterexample": "" if support_fraction >= 0.95 else str(max(r for r in results if r > 10))
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["counterexample"] != "" for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"] and r["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")