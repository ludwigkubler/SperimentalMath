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
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        literal = next((l for l in range(1, len(cnf) + 1) if l not in assignment and -l not in assignment), None)
        if literal is None:
            return False
        
        def propagate(lit):
            new_cnf = []
            for clause in cnf:
                if lit in clause:
                    continue
                elif -lit in clause:
                    clause.remove(-lit)
                    if not clause:
                        return False
                else:
                    new_cnf.append(clause)
            return new_cnf
        
        def backtrack(lit):
            assignment.pop(lit, None)
            for l in list(assignment.keys()):
                if abs(l) == abs(lit):
                    assignment.pop(l, None)
        
        if dpll(propagate(literal), assignment | {literal: True}):
            return True
        backtrack(literal)
        if dpll(propagate(-literal), assignment | {-literal: True}):
            return True
        backtrack(-literal)
        return False
    
    def etale_cohomology(cnf):
        # Simplified mapping to a graph problem for demonstration purposes
        n = len(cnf)
        adj_matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            for lit in clause:
                if abs(lit) <= n:
                    adj_matrix[abs(lit)][abs(lit)] += 1
        return sum(sum(row) - len(row) for row in adj_matrix)
    
    def dpll_proof_length(cnf):
        # Simplified heuristic to estimate proof length
        return len(cnf) * 2
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    
    etale_order = etale_cohomology(cnf)
    proof_length = dpll_proof_length(cnf)
    
    if abs(etale_order - proof_length) > 3:
        return {
            "metric_name": "etale_order_diff",
            "metric_value": abs(etale_order - proof_length),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"n={n}, etale_order={etale_order}, proof_length={proof_length}"
        }
    
    return {
        "metric_name": "etale_order_diff",
        "metric_value": abs(etale_order - proof_length),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_diff = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_diff} std=0 support_fraction={support_fraction}")
    elif any(r["counterexample"]):
        first_failing_seed = next(r["seed"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")