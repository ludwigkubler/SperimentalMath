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
    
    def is_quadratic_residue(a, p):
        if a == 0:
            return True
        for i in range(1, p):
            if (i * i) % p == a:
                return True
        return False
    
    def count_quadratic_residues(p):
        return sum(is_quadratic_residue(a, p) for a in range(p))
    
    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        var = next((v for v in range(1, len(cnf) + 1) if v not in assignment and -v not in assignment), None)
        if var is None:
            return False
        
        def propagate(var_value):
            new_assignment = assignment.copy()
            new_assignment[var] = var_value
            new_cnf = []
            for clause in cnf:
                if any(lit in new_assignment and new_assignment[lit] == (lit > 0) for lit in clause):
                    continue
                elif all(lit not in new_assignment or new_assignment[lit] != (lit > 0) for lit in clause):
                    return None
                else:
                    new_clause = [lit for lit in clause if lit not in new_assignment]
                    new_cnf.append(new_clause)
            return new_cnf, new_assignment
        
        result_true = dpll(propagate(True)[0], propagate(True)[1])
        if result_true:
            return True
        result_false = dpll(propagate(False)[0], propagate(False)[1])
        return result_false
    
    def generate_random_cnf(n):
        cnf = []
        for _ in range(2 * n):
            clause = random.sample(range(-n, 0), 1) + random.sample(range(1, n + 1), 2)
            cnf.append(clause)
        return cnf
    
    def order_of_multiplicative_group(p):
        if p <= 1:
            raise ValueError("p must be greater than 1")
        for i in range(2, p):
            if pow(i, p - 1, p) == 1:
                return p - 1
        return 1
    
    n = 30
    cnf = generate_random_cnf(n)
    p = order_of_multiplicative_group(2 * n + 1)
    num_quadratic_residues = count_quadratic_residues(p)
    log_residues = math.log(num_quadratic_residues, 2)
    
    dpll_height = dpll(cnf)
    
    if dpll_height is None:
        return {
            "metric_name": "DPLL height",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "DPLL search tree failed to terminate"
        }
    
    return {
        "metric_name": "DPLL height",
        "metric_value": dpll_height,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(dpll_height - log_residues) <= 3,
        "counterexample": "" if abs(dpll_height - log_residues) <= 3 else f"DPLL height: {dpll_height}, Log residues: {log_residues}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
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
    elif any(abs(r["metric_value"] - math.log(count_quadratic_residues(order_of_multiplicative_group(2 * 30 + 1)), 2)) > 3 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if abs(result["metric_value"] - math.log(count_quadratic_residues(order_of_multiplicative_group(2 * 30 + 1)), 2)) > 3)
        print(f"RESULT: FALSIFIED counterexample=\"DPLL height does not match log residues\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=budget_exceeded n_tested={len(results)}")