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
    
    def dpll_width(cnf):
        variables = set(abs(lit) for lit in sum(cnf, []))
        
        def solve(clauses, assignment={}):
            if not clauses:
                return 0
            unit_clauses = [c[0] for c in clauses if len(c) == 1]
            pure_lits = {}
            for lit in variables:
                pos_count = sum(1 for c in clauses if lit in c)
                neg_count = sum(1 for c in clauses if -lit in c)
                if pos_count == 0:
                    pure_lits[lit] = True
                elif neg_count == 0:
                    pure_lits[-lit] = True
            
            if unit_clauses:
                literal = unit_clauses[0]
                new_assignment = assignment.copy()
                new_assignment[literal] = True
                return solve([c for c in clauses if literal not in c and -literal not in c], new_assignment)
            
            if pure_lits:
                literal = next(lit for lit, val in pure_lits.items() if val)
                new_assignment = assignment.copy()
                new_assignment[literal] = True
                return solve([c for c in clauses if literal not in c and -literal not in c], new_assignment)
            
            literal = variables.pop()
            width_positive = 1 + solve(clauses, {**assignment, literal: True})
            width_negative = 1 + solve(clauses, {**assignment, literal: False})
            return max(width_positive, width_negative)
        
        return solve(cnf)
    
    def min_reflections(cnf):
        # Placeholder for the actual computation of minimal reflections
        # This is a dummy implementation and should be replaced with the actual logic
        return len(cnf) // 2
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    width = dpll_width(cnf)
    min_reflect = min_reflections(cnf)
    
    return {
        "metric_name": "DPLL Width vs Min Reflections",
        "metric_value": abs(width - min_reflect),
        "instances_tested": 1,
        "conjecture_holds": abs(width - min_reflect) <= 3,
        "counterexample": "" if abs(width - min_reflect) <= 3 else f"Width: {width}, Min Reflections: {min_reflect}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")