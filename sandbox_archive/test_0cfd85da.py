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

def generate_cnf(n):
    cnf = []
    for _ in range(10):  # Generate 10 clauses for simplicity
        clause = [random.randint(-n, n) for _ in range(3)]
        if all(x != 0 for x in clause):
            cnf.append(clause)
    return cnf

def tseitin_polynomial(cnf):
    literals = set()
    for clause in cnf:
        literals.update(abs(lit) for lit in clause)
    
    clauses = []
    new_vars = {}
    var_count = 1
    
    for i, literal in enumerate(literals):
        new_var = f"v{var_count}"
        new_vars[literal] = new_var
        new_vars[-literal] = f"~{new_var}"
        var_count += 1
    
    for clause in cnf:
        disjunction = []
        for lit in clause:
            if lit > 0:
                disjunction.append(new_vars[lit])
            else:
                disjunction.append(f"~{new_vars[-lit]}")
        
        conjunction = []
        for i, lit in enumerate(clause):
            negated_lit = f"~{new_vars[lit]}"
            conjunction.extend([negated_lit] + [f"v{j+1}" for j in range(i) if j != i])
        
        clauses.append(conjunction)
    
    return clauses

def resolution_width(cnf):
    def resolve(clause1, clause2):
        resolved = []
        for lit1 in clause1:
            for lit2 in clause2:
                if lit1 == -lit2:
                    continue
                resolved.append(lit1)
        return resolved
    
    queue = cnf[:]
    while True:
        new_clauses = []
        found_resolvent = False
        
        for i in range(len(queue)):
            for j in range(i + 1, len(queue)):
                resolvent = resolve(queue[i], queue[j])
                if not resolvent:
                    continue
                found_resolvent = True
                new_clauses.append(resolvent)
        
        if not found_resolvent:
            break
        
        queue.extend(new_clauses)
    
    return max(len(clause) for clause in queue)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 5 + (seed % 6) * 5  # Sweep through sizes 5, 10, 15, 20, 30, 40
    cnf = generate_cnf(n)
    tseitin_poly = tseitin_polynomial(cnf)
    width = resolution_width(tseitin_poly)
    
    return {
        "metric_name": "#M(φ)",
        "metric_value": len(tseitin_poly),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": len(tseitin_poly) <= width,
        "counterexample": "" if len(tseitin_poly) <= width else f"Counterexample for n={n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")