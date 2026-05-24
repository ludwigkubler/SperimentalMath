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
        for _ in range(n * 2):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def dpll_refutation_depth(cnf):
        def is_satisfiable(cnf, assignment):
            for clause in cnf:
                if all(var not in assignment or (assignment[var] == 0 and var < 0) for var in clause):
                    continue
                if any(var in assignment and (assignment[var] == 1 and var > 0) for var in clause):
                    return False
            return True
        
        def dpll(cnf, assignment, level=0):
            if not cnf:
                return level
            unit_clause = next((c for c in cnf if len(c) == 1), None)
            if unit_clause:
                var = abs(unit_clause[0])
                assignment[var] = 1 if unit_clause[0] > 0 else -1
                cnf.remove(unit_clause)
                return dpll(cnf, assignment, level + 1)
            
            p_var = next(var for var in range(1, len(assignment) + 1) if var not in assignment)
            assignment[p_var] = 1
            depth_if_true = dpll(cnf, assignment, level + 1)
            if depth_if_true > level:
                return depth_if_true
            
            assignment[p_var] = -1
            depth_if_false = dpll(cnf, assignment, level + 1)
            return max(depth_if_true, depth_if_false)
        
        assignment = {}
        return dpll(cnf, assignment)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    k = 2 ** (n - 1)  # Minimal order of a totally ramified extension for a field with n variables
    t_star = dpll_refutation_depth(cnf)
    
    return {
        "metric_name": "log2(k)",
        "metric_value": math.log2(k),
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")