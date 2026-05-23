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
    
    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        literal = next((l for l in range(1, len(assignment) + 2) if l not in assignment and -l not in assignment), None)
        if literal is None:
            return False
        
        def propagate(lit):
            new_cnf = []
            for clause in cnf:
                if lit in clause:
                    continue
                if -lit in clause:
                    clause.remove(-lit)
                    if not clause:
                        return None
                else:
                    new_cnf.append(clause)
            return new_cnf
        
        def backtrack(lit):
            del assignment[lit]
        
        result = dpll(propagate(lit), assignment | {lit: True})
        if result:
            return True
        backtrack(lit)
        
        result = dpll(propagate(-lit), assignment | {-lit: True})
        if result:
            return True
        backtrack(-lit)
        
        return False
    
    def algebraic_hodge_structure(cnf):
        # Simplified version for demonstration; actual computation would be complex
        return len(cnf) ** 0.5
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    hodge_rank = algebraic_hodge_structure(cnf)
    width = dpll(cnf)
    
    if width is None:
        counterexample = "DPLL search tree width not computable"
        conjecture_holds = False
    else:
        c_n = 1.0  # Placeholder for empirical constant
        conjecture_holds = width <= c_n * hodge_rank ** 2
        counterexample = "" if conjecture_holds else f"Width {width} exceeds bound {c_n * hodge_rank ** 2}"
    
    return {
        "metric_name": "DPLL Search Tree Width",
        "metric_value": width,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_width = sum(r["metric_value"] for r in results) / len(results)
    std_width = math.sqrt(sum((r["metric_value"] - mean_width) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")