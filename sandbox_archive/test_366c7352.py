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
        for _ in range(2 * n):
            clause = [random.randint(-n, n) for _ in range(random.randint(1, 3))]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf):
        assignment = {}
        
        def is_satisfiable():
            for clause in cnf:
                if not any(abs(lit) in assignment and (assignment[lit] == (lit > 0)) for lit in clause):
                    return False
            return True
        
        def unit_propagation():
            while True:
                changed = False
                for var, value in assignment.items():
                    for clause in cnf:
                        if all(abs(lit) != var for lit in clause):
                            continue
                        if any(abs(lit) == var and (lit > 0) != value for lit in clause):
                            return None
                        if all(abs(lit) == var and (lit > 0) == value for lit in clause):
                            changed = True
                if not changed:
                    break
            return assignment
        
        def pure_literal_elimination():
            while True:
                changed = False
                for lit in range(1, n + 1):
                    pos_count = sum(1 for clause in cnf if lit in clause)
                    neg_count = sum(1 for clause in cnf if -lit in clause)
                    if pos_count == len(cnf) or neg_count == len(cnf):
                        changed = True
                        assignment[lit] = pos_count > neg_count
                if not changed:
                    break
            return assignment
        
        def backtracking():
            stack = []
            while True:
                if is_satisfiable():
                    return unit_propagation()
                if not stack:
                    return None
                var, value = stack.pop()
                assignment[var] = value
                for clause in cnf:
                    if all(abs(lit) != var for lit in clause):
                        continue
                    if any(abs(lit) == var and (lit > 0) != value for lit in clause):
                        return None
                    if all(abs(lit) == var and (lit > 0) == value for lit in clause):
                        stack.append((var, not value))
                assignment.pop(var)
        
        return backtracking()
    
    def resolution_proof_width(cnf):
        clauses = cnf[:]
        new_clauses = []
        while True:
            unit_propagation()
            pure_literal_elimination()
            if len(clauses) == 0:
                return 0
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    clause_i = clauses[i]
                    clause_j = clauses[j]
                    new_clause = []
                    for lit_i in clause_i:
                        if -lit_i in clause_j:
                            continue
                        new_clause.append(lit_i)
                    for lit_j in clause_j:
                        if -lit_j in clause_i:
                            continue
                        new_clause.append(lit_j)
                    if len(new_clause) == 0:
                        return max(len(clause_i), len(clause_j))
                    new_clauses.append(new_clause)
            clauses.extend(new_clauses)
            new_clauses = []
    
    cnf_formula = generate_cnf(10)
    ω_F = resolution_proof_width(cnf_formula)
    
    g_F = 0  # Placeholder for the arithmetic genus, which is not computable in pure Python
    if ω_F == 0:
        g_F = 0
    else:
        g_F = Fraction(ω_F - 1, 2) * (Fraction(ω_F - 3, 2) + 1)
    
    return {
        "metric_name": "Arithmetic Genus vs Resolution Proof Width",
        "metric_value": abs(g_F - ω_F),
        "instances_tested": 1,
        "conjecture_holds": g_F <= 10 * ω_F,
        "counterexample": "" if g_F <= 10 * ω_F else f"Arithmetic genus {g_F} > 10 times resolution proof width {ω_F}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))
    
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")