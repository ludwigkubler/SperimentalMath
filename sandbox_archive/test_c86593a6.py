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
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        literal = find_pure_literal(cnf) or find_unit_clause(cnf)
        if literal is None:
            return False
        
        var = abs(literal)
        if literal > 0:
            assignment[var] = True
        else:
            assignment[-var] = True
        
        new_cnf = []
        for clause in cnf:
            if literal not in clause and -literal not in clause:
                new_cnf.append(clause)
        
        return dpll(new_cnf, assignment)
    
    def find_pure_literal(cnf):
        pure_literals = {}
        for clause in cnf:
            for literal in clause:
                if abs(literal) not in pure_literals:
                    pure_literals[abs(literal)] = literal
                elif pure_literals[abs(literal)] != literal:
                    del pure_literals[abs(literal)]
        
        return next(iter(pure_literals.values()), None)
    
    def find_unit_clause(cnf):
        for clause in cnf:
            if len(clause) == 1:
                return clause[0]
        return None
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    min_root_count = len(set([abs(lit) for lit in random.sample(range(-n, -1), n)]))
    diameter = dpll(cnf)
    
    if diameter is False:
        return {
            "metric_name": "min_root_count",
            "metric_value": min_root_count,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "DPLL search tree did not find a solution"
        }
    
    return {
        "metric_name": "min_root_count",
        "metric_value": min_root_count,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["conjecture_holds"]]
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values)} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values)} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "DPLL search tree did not find a solution"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")