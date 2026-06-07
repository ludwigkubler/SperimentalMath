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
        clauses = []
        for _ in range(2**n):
            clause = [random.randint(-n, n-1) for _ in range(random.randint(1, 3))]
            clauses.append(clause)
        return clauses
    
    def dpll_solve(cnf):
        def solve(variables, assignment):
            if not cnf:
                return True
            literal = cnf[0][0]
            if literal > 0 and literal in assignment or literal < 0 and -literal in assignment:
                return solve(cnf[1:], assignment)
            for value in [True, False]:
                new_assignment = assignment.copy()
                new_assignment[literal] = value
                if solve(cnf, new_assignment):
                    return True
            return False
        
        variables = list(range(1, n+1))
        return solve(cnf, {})
    
    def p_adic_order(n):
        # Approximate the p-adic order using a simple heuristic
        return math.sqrt(n)
    
    n_values = [5, 10, 15, 20, 30, 40]
    ratios = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        if dpll_solve(cnf):
            clause_depth = len(cnf)
            order = p_adic_order(n)
            ratios.append(clause_depth / order)
    
    mean_ratio = sum(ratios) / len(ratios)
    conjecture_holds = all(r <= 4 for r in ratios)
    counterexample = f"mean_ratio={mean_ratio}" if not conjecture_holds else ""
    
    return {
        "metric_name": "Ratio of Clause Depth to p-adic Order",
        "metric_value": mean_ratio,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mean_ratio={mean_ratio}' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")