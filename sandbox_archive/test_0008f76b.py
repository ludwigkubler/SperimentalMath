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
        cnf = []
        for _ in range(n):
            clause = [random.randint(1, n*2) for _ in range(random.randint(1, 3))]
            cnf.append(clause)
        return cnf
    
    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        unit_clauses = [c[0] for c in cnf if len(c) == 1]
        pure_literals = {}
        for clause in cnf:
            for literal in clause:
                sign = literal > 0
                var = abs(literal)
                if var not in pure_literals:
                    pure_literals[var] = (sign, 1)
                else:
                    if pure_literals[var][0] != sign:
                        return False
                    pure_literals[var] = (sign, pure_literals[var][1] + 1)
        
        for var, (sign, count) in pure_literals.items():
            if count == len(cnf):
                assignment[var] = sign
                new_cnf = [c for c in cnf if not any(lit in c for lit in [-var, var])]
                return dpll(new_cnf, assignment)
        
        literal = random.choice([lit for clause in cnf for lit in clause])
        sign = literal > 0
        var = abs(literal)
        assignment[var] = sign
        new_cnf = [c for c in cnf if not any(lit in c for lit in [-var, var])]
        
        if dpll(new_cnf, assignment):
            return True
        
        del assignment[var]
        assignment[var] = not sign
        new_cnf = [c for c in cnf if not any(lit in c for lit in [-var, var])]
        
        return dpll(new_cnf, assignment)
    
    def diophantine_exponent(cnf):
        n = len(cnf)
        for d in range(1, 2*n + 1):
            Z_d = [i % d for i in range(n)]
            if all(any(lit % d == Z_d[var-1] for lit in clause) for clause in cnf):
                return d
        return n
    
    def dpll_refutation_time(cnf):
        start_time = time.time()
        dpll(cnf)
        end_time = time.time()
        return end_time - start_time
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        cnf = generate_cnf(n)
        d = diophantine_exponent(cnf)
        ref_time = dpll_refutation_time(cnf)
        if ref_time == 0:
            continue
        ratio = n**d * math.log(n) / ref_time
        results.append(ratio)
    
    mean_ratio = sum(results) / len(results)
    conjecture_holds = mean_ratio <= 3
    
    return {
        "metric_name": "Ratio of n^d(φ) * log(n) to DPLL refutation time",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": max([random.choice([5, 10, 15, 20, 30, 40]) for _ in range(30)]),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "Ratio exceeded 3"
    }

if __name__ == "__main__":
    import time
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean_ratio = sum(results) / len(results)
    support_fraction = sum(1 for r in results if r <= 3) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={math.sqrt(sum((r - mean_ratio)**2 for r in results) / len(results))} support_fraction={support_fraction}")
    elif any(r > 3 for r in results):
        first_failing_seed = seeds[results.index(max(results))]
        print(f"RESULT: FALSIFIED counterexample='Ratio exceeded 3' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")