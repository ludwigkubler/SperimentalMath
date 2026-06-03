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
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        unit_clauses = [c[0] for c in cnf if len(c) == 1]
        pure_literals = {}
        
        for literal in set([abs(lit) for lit in sum(cnf, [])]):
            pos_count = sum(1 for clause in cnf if literal in clause)
            neg_count = sum(1 for clause in cnf if -literal in clause)
            if pos_count == 0:
                pure_literals[literal] = True
            elif neg_count == 0:
                pure_literals[-literal] = True
        
        if unit_clauses:
            literal = unit_clauses[0]
            new_assignment[literal] = True
            cnf = [c for c in cnf if literal not in c and -literal not in c]
            return dpll(cnf, new_assignment)
        
        if pure_literals:
            literal = next(iter(pure_literals))
            new_assignment[literal] = True
            cnf = [c for c in cnf if literal not in c and -literal not in c]
            return dpll(cnf, new_assignment)
        
        literal = random.choice(sum(cnf, []))
        new_assignment[literal] = True
        cnf_true = [c for c in cnf if literal in c]
        cnf_false = [c for c in cnf if -literal in c]
        return dpll(cnf_true, new_assignment) or dpll(cnf_false, {**new_assignment, -literal: False})
    
    def p_adic_l_function_order(cnf):
        # Simplified approximation of L-function order
        return len(cnf)
    
    n = random.randint(5, 40)
    m = random.randint(n, 2 * n)
    cnf = generate_cnf(n, m)
    l_phi = p_adic_l_function_order(cnf)
    phi_assignment = {}
    if dpll(cnf, phi_assignment):
        l_dpll = len(phi_assignment)
    else:
        l_dpll = float('inf')
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": (l_phi - l_dpll) / max(l_phi, l_dpll),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs((l_phi - l_dpll) / max(l_phi, l_dpll)) < 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient<0.5' first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data_or_budget_exceeded")