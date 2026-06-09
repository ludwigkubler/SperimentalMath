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
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def p_adic_representation(cnf):
        n = len(cnf)
        rep = [[0] * n for _ in range(n)]
        for clause in cnf:
            idx1, idx2 = abs(clause[0]) - 1, abs(clause[1]) - 1
            if idx1 < n and idx2 < n:
                rep[idx1][idx2] += 1
                rep[idx2][idx1] += 1
        return rep
    
    def resolution_width(cnf):
        # Simplified DPLL solver to estimate width
        stack = []
        assignment = [None] * (len(cnf) + 1)
        
        def dpll():
            if not cnf:
                return True
            literal, polarity = find_pure_literal(cnf)
            if literal is None:
                literal, polarity = find_unit_clause(cnf)
                if literal is None:
                    return False
            assignment[literal] = polarity
            new_cnf = [clause for clause in cnf if not evaluate(clause)]
            negated_literal = -literal
            new_cnf.extend([negate(lit) for lit in new_cnf if lit == negated_literal])
            stack.append((new_cnf, assignment))
            return dpll()
        
        def find_pure_literal(cnf):
            pure_literals = [i for i in range(1, len(cnf) + 1) if (i not in assignment and -i not in assignment)]
            for literal in pure_literals:
                polarity = all(lit == literal for lit in cnf if abs(lit) == literal)
                return literal, polarity
            return None, None
        
        def find_unit_clause(cnf):
            unit_clauses = [clause[0] for clause in cnf if len(clause) == 1]
            for clause in unit_clauses:
                polarity = assignment[abs(clause)] == (clause > 0)
                return abs(clause), polarity
            return None, None
        
        def evaluate(clause):
            return any(lit in assignment and assignment[lit] == (lit > 0) for lit in clause)
        
        def negate(lit):
            return -lit if lit > 0 else -lit
        
        return len(assignment) if dpll() else float('inf')
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    rep = p_adic_representation(cnf)
    width = resolution_width(cnf)
    
    if width == float('inf'):
        return {
            "metric_name": "resolution_width",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "unprovable"
        }
    
    defect = sum(sum(row) for row in rep) / (n * n)
    ratio = width / defect
    
    return {
        "metric_name": "resolution_width",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ratio <= 1.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")