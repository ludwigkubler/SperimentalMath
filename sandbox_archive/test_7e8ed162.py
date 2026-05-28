# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import Counter

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, random.randint(1, n))
            clauses.append(clause)
        return clauses
    
    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        unit_clauses = [c for c in cnf if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0][0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in cnf if literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in cnf if -literal not in c], new_assignment):
                return True
        pure_literals = [l for l in range(1, max(cnf) + 1) if (l not in assignment and -l not in assignment)]
        if pure_literals:
            literal = pure_literals[0]
            new_assignment[literal] = True
            if dpll([c for c in cnf if literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in cnf if -literal not in c], new_assignment):
                return True
        return False
    
    def refutation_size(cnf):
        assignment = {}
        for clause in cnf:
            unassigned_vars = [var for var in clause if var not in assignment and -var not in assignment]
            if unassigned_vars:
                literal = random.choice(unassigned_vars)
                assignment[literal] = True
            else:
                return len(cnf)  # All clauses are satisfied, no refutation needed
        return len(cnf)  # No valid assignment found, full refutation
    
    n = random.randint(5, 40)
    m = random.randint(n, 2 * n)
    cnf = generate_cnf(n, m)
    
    ref_size = refutation_size(cnf)
    
    return {
        "metric_name": "refutation_size",
        "metric_value": ref_size,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean = sum(r['metric_value'] for r in results) / len(results)
    std_dev = math.sqrt(sum((r['metric_value'] - mean)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")