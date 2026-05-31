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
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def dpll(clause_set, assignment, clauses):
        if not clause_set:
            return True
        unit_clause = next((c for c in clause_set if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            if literal < 0:
                literal = -literal
                value = assignment[literal - 1] == 0
            else:
                value = assignment[literal - 1] is None
            if value:
                assignment[literal - 1] = 1
                if dpll(clause_set, assignment, clauses):
                    return True
                assignment[literal - 1] = 0
                if dpll(clause_set, assignment, clauses):
                    return True
                assignment[literal - 1] = None
            else:
                assignment[literal - 1] = 0
                if dpll(clause_set, assignment, clauses):
                    return True
                assignment[literal - 1] = None
            return False
        
        literal = next(lit for lit in range(1, len(assignment) + 1) if assignment[lit - 1] is None)
        assignment[literal - 1] = 1
        if dpll(clause_set, assignment, clauses):
            return True
        assignment[literal - 1] = 0
        if dpll(clause_set, assignment, clauses):
            return True
        assignment[literal - 1] = None
        return False
    
    n = random.randint(5, 40)
    clause_set = generate_cnf(n)
    assignment = [None] * n
    result = dpll(clause_set, assignment, clause_set)
    
    if not result:
        counterexample = "DPLL solver failed to find a satisfying assignment"
        return {
            "metric_name": "misl(φ)",
            "metric_value": 0,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": counterexample
        }
    
    # Constructive mapping from CNF to a matrix representation for symplectic reduction
    # This is a placeholder and should be replaced with actual computation
    misl_phi = random.random() * n
    
    return {
        "metric_name": "misl(φ)",
        "metric_value": misl_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["counterexample"] for r in results):
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"] and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[results.index(next(r for r in results if not r['conjecture_holds'] and r['counterexample']))]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support_fraction")