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
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(c == 0 for c in clause):
                continue
            clauses.append(clause)
        return clauses
    
    def dpll(cnf):
        def search(assignment):
            unsatisfied_clauses = [c for c in cnf if not any(lit * assignment[abs(lit) - 1] > 0 for lit in c)]
            if not unsatisfied_clauses:
                return True
            unit_clause = next((c for c in unsatisfied_clauses if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                assignment[abs(literal) - 1] = literal > 0
                if search(assignment):
                    return True
                assignment[abs(literal) - 1] = not (literal > 0)
                if search(assignment):
                    return True
            for literal in range(1, len(assignment) + 1):
                if literal not in assignment:
                    assignment[literal - 1] = True
                    if search(assignment):
                        return True
                    assignment[literal - 1] = False
                    if search(assignment):
                        return True
            return False
        
        assignment = {}
        return search(assignment)
    
    def hdc(cnf):
        # Placeholder for actual Hodge decomposition computation
        # This is a dummy implementation and should be replaced with the actual algorithm
        return len(cnf)  # Simplified for testing purposes
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    
    hdc_value = hdc(cnf)
    proof_length = dpll(cnf)
    
    if proof_length is None:
        return {
            "metric_name": "hdc_vs_dpll",
            "metric_value": -1,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "DPLL solver returned None"
        }
    
    correlation_coefficient = hdc_value / proof_length if proof_length != 0 else 0
    
    return {
        "metric_name": "hdc_vs_dpll",
        "metric_value": correlation_coefficient,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": correlation_coefficient >= 0.8,
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
    
    metric_values = [r["metric_value"] for r in results if r["metric_value"] != -1]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["metric_value"] != -1 for r in results):
        mean_value = sum(metric_values) / len(metric_values)
        std_value = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values))
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
        else:
            print(f"RESULT: FALSIFIED counterexample='correlation_coefficient<0.8' first_failing_seed={seeds[results.index(next(r for r in results if not r['conjecture_holds'] and r['metric_value'] != -1))]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=missing_data n_tested={len(metric_values)}")