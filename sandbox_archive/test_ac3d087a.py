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
    
    def resolution_width(phi):
        clauses = phi.split(' or ')
        variables = set()
        for clause in clauses:
            literals = clause.split(' and ')
            for literal in literals:
                if literal.startswith('not '):
                    literal = literal[4:]
                variables.add(literal)
        
        assignment = {var: False for var in variables}
        
        def dpll(clauses, assignment):
            if not clauses:
                return True
            unit_clauses = [c for c in clauses if len(c.split(' and ')) == 1]
            if unit_clauses:
                literal = unit_clauses[0].split(' and ')[0]
                if literal.startswith('not '):
                    literal = literal[4:]
                    assignment[literal] = False
                else:
                    assignment[literal] = True
                clauses = [c for c in clauses if literal not in c and 'not ' + literal not in c]
            pure_literals = {}
            for var in variables:
                pos_count, neg_count = 0, 0
                for clause in clauses:
                    literals = clause.split(' and ')
                    if var in literals:
                        pos_count += 1
                    elif 'not ' + var in literals:
                        neg_count += 1
                if pos_count == 0:
                    pure_literals[var] = False
                elif neg_count == 0:
                    pure_literals[var] = True
            for literal, value in pure_literals.items():
                assignment[literal] = value
                clauses = [c for c in clauses if literal not in c and 'not ' + literal not in c]
            if not clauses:
                return True
            literal = random.choice([l for clause in clauses for l in clause.split(' and ')])
            if literal.startswith('not '):
                literal = literal[4:]
                assignment[literal] = False
            else:
                assignment[literal] = True
            new_clauses = []
            for clause in clauses:
                literals = clause.split(' and ')
                if literal not in literals and 'not ' + literal not in literals:
                    new_clauses.append(clause)
            return dpll(new_clauses, assignment)
        
        return len(assignment) if dpll(clauses, assignment) else 0
    
    def minimal_hodge_index(phi):
        # Placeholder for the actual Hodge index computation
        # This is a dummy implementation and should be replaced with a proper one
        return random.randint(1, 5)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    k = random.randint(1, min(n-1, 5))
    phi = ' or '.join(' and '.join(random.sample(['x' + str(i) for i in range(n)], k)) for _ in range(k+1))
    
    w_phi = resolution_width(phi)
    H_phi = minimal_hodge_index(phi)
    
    if w_phi is None or H_phi is None:
        return {
            "metric_name": "resolution_width",
            "metric_value": 0,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    metric_value = math.log2(n**(k+1)) <= w_phi + H_phi
    
    return {
        "metric_name": "resolution_width",
        "metric_value": float(metric_value),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": metric_value,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")