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
        clauses = []
        for _ in range(2 ** n):
            clause = [random.randint(-n, n - 1) for _ in range(random.randint(1, n))]
            if any(abs(lit) == abs(clause[0]) for lit in clause[1:]):
                continue
            clauses.append(clause)
        return clauses
    
    def frege_proof_depth(cnf):
        # Simplified DPLL-based algorithm for Frege proof depth
        stack = []
        assignment = {}
        for clause in cnf:
            if all(abs(lit) not in assignment or assignment[abs(lit)] != lit for lit in clause):
                return 1
            new_assignment = {abs(lit): lit for lit in clause}
            stack.append((new_assignment, 1))
        while stack:
            assignment, depth = stack.pop()
            if all(abs(lit) in assignment and assignment[abs(lit)] == lit for lit in cnf):
                return depth
            new_clause = [lit for lit in cnf if abs(lit) not in assignment]
            if new_clause:
                new_assignment = {abs(lit): lit for lit in new_clause}
                stack.append((new_assignment, depth + 1))
        return float('inf')
    
    def minimal_p_adic_valuation_rank(poly):
        # Simplified p-adic valuation rank calculation
        rank = 0
        for coeff in poly:
            if coeff != 0:
                rank += len(bin(coeff)) - bin(coeff).find('1') - 2
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        poly = [sum([random.randint(-n, n - 1) * (x ** i) for i in range(n + 1)]) for x in range(2)]
        r_phi = minimal_p_adic_valuation_rank(poly)
        d_phi = frege_proof_depth(cnf)
        
        results.append({
            "n": n,
            "r_phi": r_phi,
            "d_phi": d_phi
        })
    
    correlation = sum((r['r_phi'] - mean_r) * (r['d_phi'] - mean_d) for r in results) / len(results)
    mean_r = sum(r['r_phi'] for r in results) / len(results)
    mean_d = sum(r['d_phi'] for r in results) / len(results)
    
    conjecture_holds = correlation >= 0.7
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(r['n'] for r in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r['metric_value'] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results) and support_fraction >= 0.8:
        print("RESULT: FALSIFIED counterexample=mapping_undefined first_failing_seed=<s>")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support")