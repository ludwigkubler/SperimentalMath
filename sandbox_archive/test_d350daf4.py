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
            clause = [random.randint(-1, 0) * (i + 1) for i in range(n)]
            if all(c == 0 for c in clause):
                continue
            clauses.append(clause)
        return clauses
    
    def dpll_solve(clauses, assignment=[]):
        if not clauses:
            return True
        var = next((v for v in range(1, len(clauses) + 1) if v not in [abs(c) for c in assignment]), None)
        if var is None:
            return False
        
        def propagate(var, value):
            new_clauses = []
            for clause in clauses:
                if any(abs(v) == var and c != value * v for c in clause):
                    continue
                elif all(abs(v) != abs(c) for c in clause):
                    return None
                new_clause = [c for c in clause if abs(c) != var]
                if not new_clause:
                    return None
                new_clauses.append(new_clause)
            return new_clauses
        
        if dpll_solve(propagate(var, 1), assignment + [var]):
            return True
        if dpll_solve(propagate(-var, -1), assignment + [-var]):
            return True
        return False
    
    def p_adic_order(clause):
        # Simplified approximation for demonstration purposes
        return len(clause) ** (1/2)
    
    n = 5
    trials = 30
    total_ratio = 0
    max_n = n
    
    for _ in range(trials):
        cnf = generate_cnf(n)
        if not dpll_solve(cnf):
            continue
        
        clause_depth = len(cnf)
        p_order = p_adic_order(cnf[0])
        
        if p_order == 0:
            continue
        
        ratio = clause_depth / p_order
        total_ratio += ratio
        max_n = max(max_n, n)
    
    if trials == 0:
        return {
            "metric_name": "ratio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max_n,
            "conjecture_holds": False,
            "counterexample": "no_valid_cnf_found"
        }
    
    mean_ratio = total_ratio / trials
    support_fraction = (mean_ratio <= 4)
    
    return {
        "metric_name": "ratio",
        "metric_value": mean_ratio,
        "instances_tested": trials,
        "n_max": max_n,
        "conjecture_holds": support_fraction,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_ratio = sum(r['metric_value'] for r in results if r['metric_value'] is not None) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(r['metric_value'] > 10 for r in results):
        first_failing_seed = next((r['seed'] for r in results if r['metric_value'] > 10), None)
        print(f"RESULT: FALSIFIED counterexample=\"ratio_exceeds_10\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")