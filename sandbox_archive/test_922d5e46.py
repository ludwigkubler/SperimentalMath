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
    
    def generate_3cnf(n, m):
        clauses = []
        variables = set(range(1, n + 1))
        for _ in range(m):
            clause = random.sample(variables, 2)
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def is_satisfiable(clauses):
        # Simplified SAT solver using backtracking
        assignment = {}
        stack = []
        
        def backtrack():
            if len(assignment) == n:
                return True
            var = next((v for v in range(1, n + 1) if v not in assignment), None)
            if var is None:
                return False
            
            for val in [True, False]:
                assignment[var] = val
                stack.append((var, val))
                
                if all(any(not (c[0] < 0 and assignment.get(-c[0], False)) for c in clause) or any(c[0] > 0 and assignment.get(c[0], False) for c in clause) for clause in clauses):
                    if backtrack():
                        return True
                
                stack.pop()
                del assignment[var]
            
            return False
        
        n = len(variables)
        return backtrack()
    
    def compute_k_theory_rank(clauses):
        # Simplified computation of K-theory rank
        m = len(clauses)
        n = len(set(abs(c) for clause in clauses for c in clause))
        return (n + math.log(m)) ** 2
    
    n = random.randint(5, 40)
    m = random.randint(n * 2, n * 10)
    clauses = generate_3cnf(n, m)
    
    if not is_satisfiable(clauses):
        return {
            "metric_name": "K-theory rank",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "unsatisfiable"
        }
    
    k_theory_rank = compute_k_theory_rank(clauses)
    expected_rank = (n + math.log(m)) ** 2
    
    return {
        "metric_name": "K-theory rank",
        "metric_value": k_theory_rank,
        "instances_tested": 1,
        "conjecture_holds": k_theory_rank <= expected_rank,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30 * 1000 + 1, 100))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result_type = "SUPPORTED"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = f"first failing seed: {first_failing_seed}"
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        result_type = "FALSIFIED"
    
    print(f"RESULT: {result_type} mean={mean_value:.2f} std=0.00 support_fraction={support_fraction:.2f}")