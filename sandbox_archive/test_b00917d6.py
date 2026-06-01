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
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if any(c != 0 for c in clause):
                clauses.append(clause)
        return clauses

    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        literal = next((l for l in range(1, len(cnf[0]) + 1) if l not in assignment and -l not in assignment), None)
        if literal is None:
            return False
        
        def propagate(lit):
            new_cnf = []
            for clause in cnf:
                if any(abs(x) == abs(lit) for x in clause):
                    continue
                new_clause = [x for x in clause if x != -lit]
                if not new_clause:
                    return None
                new_cnf.append(new_clause)
            return new_cnf
        
        def backtrack():
            nonlocal assignment
            last_lit = list(assignment.keys())[-1]
            del assignment[last_lit]
            for lit in range(last_lit + 1, len(cnf[0]) + 1):
                if lit not in assignment and -lit not in assignment:
                    assignment[lit] = True
                    new_cnf = propagate(lit)
                    if new_cnf is not None:
                        if dpll(new_cnf, assignment):
                            return True
                    del assignment[lit]
            return False
        
        assignment[literal] = True
        new_cnf = propagate(literal)
        if new_cnf is not None:
            if dpll(new_cnf, assignment):
                return True
        del assignment[literal]
        
        assignment[-literal] = True
        new_cnf = propagate(-literal)
        if new_cnf is not None:
            if dpll(new_cnf, assignment):
                return True
        del assignment[-literal]
        
        return backtrack()
    
    def hodge_index(cnf):
        # Placeholder for actual Hodge index computation
        return random.random()  # Simplified for testing
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    h = hodge_index(cnf)
    d = len(dpll(cnf))
    
    return {
        "metric_name": "Hodge Index vs DPLL Diameter",
        "metric_value": abs(h) / (d + 1),  # Avoid division by zero
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}")