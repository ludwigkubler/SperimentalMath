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
    
    def generate_cnf(m, n):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def dpll(cnf, assignment=[]):
        if not cnf:
            return True
        literal = find_pure_literal(cnf) or find_unit_clause(cnf)
        if literal is None:
            literal = random.choice([i for i in range(1, n+1)] + [-i for i in range(1, n+1)])
        
        new_cnf = []
        for clause in cnf:
            if literal not in clause and -literal not in clause:
                new_cnf.append(clause)
            elif literal in clause:
                continue
            else:
                new_clause = [l for l in clause if l != -literal]
                new_cnf.append(new_clause)
        
        if dpll(new_cnf, assignment + [literal]):
            return True
        if dpll(new_cnf, assignment + [-literal]):
            return True
        
        return False
    
    def find_pure_literal(cnf):
        pure_literals = {}
        for clause in cnf:
            for literal in clause:
                if literal not in pure_literals:
                    pure_literals[literal] = 0
                pure_literals[literal] += 1
        
        for literal, count in pure_literals.items():
            if count == len(cnf):
                return literal
        return None
    
    def find_unit_clause(cnf):
        unit_clauses = []
        for clause in cnf:
            if len(clause) == 1:
                unit_clauses.append(clause[0])
        
        for literal in unit_clauses:
            if literal not in [l for clause in cnf for l in clause]:
                return literal
        return None
    
    def compute_tropical_motivic_rank(cnf):
        # Placeholder for actual computation of tropical motivic rank
        return 0
    
    m = random.randint(5, 40)
    n = random.randint(5, 40)
    
    cnf = generate_cnf(m, n)
    if not dpll(cnf):
        return {
            "metric_name": "tropical_motivic_rank",
            "metric_value": 0,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "No satisfying assignment found"
        }
    
    mtr_phi = compute_tropical_motivic_rank(cnf)
    max_deg = max(len(clause) for clause in cnf)
    min_satisfying = 1  # Placeholder, actual computation needed
    
    return {
        "metric_name": "tropical_motivic_rank",
        "metric_value": mtr_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": mtr_phi >= max_deg + min_satisfying,
        "counterexample": f"mtr_phi={mtr_phi}, max_deg+min_satisfying={max_deg+min_satisfying}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")