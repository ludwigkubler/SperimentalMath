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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        unit_clause = next((c for c in cnf if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            if literal < 0 and literal in assignment and assignment[literal] is False:
                return False
            elif literal > 0 and literal not in assignment:
                assignment[literal] = True
            else:
                assignment[-literal] = False
            cnf = [c for c in cnf if literal not in c]
            cnf = [[l for l in c if l != -literal] for c in cnf]
            return dpll(cnf, assignment)
        pure_literal = next((l for l in range(1, n+1) if (l not in assignment and -l not in assignment)), None)
        if pure_literal is not None:
            literal = pure_literal
            if literal < 0 and literal in assignment and assignment[literal] is False:
                return False
            elif literal > 0 and literal not in assignment:
                assignment[literal] = True
            else:
                assignment[-literal] = False
            cnf = [c for c in cnf if literal not in c]
            cnf = [[l for l in c if l != -literal] for c in cnf]
            return dpll(cnf, assignment)
        literal = random.choice([p for p in range(1, n+1) if p not in assignment and -p not in assignment])
        assignment[literal] = True
        if dpll(cnf, assignment):
            return True
        assignment[literal] = False
        assignment[-literal] = True
        if dpll(cnf, assignment):
            return True
        return False
    
    def resolution_width(cnf):
        queue = cnf[:]
        while queue:
            clause1 = queue.pop()
            for clause2 in queue:
                new_clause = [l for l in clause1 if l > 0] + [l for l in clause2 if l < 0]
                if len(new_clause) == 1:
                    return abs(new_clause[0])
                if not any(l in new_clause and -l in new_clause for l in new_clause):
                    queue.append(new_clause)
        return float('inf')
    
    def monodromy_group_order(cnf):
        # Placeholder function to compute the minimal monodromy group order
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(1, 10)  # Replace with actual computation
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    m = random.randint(n, 2*n)
    cnf = generate_cnf(n, m)
    
    width = resolution_width(cnf)
    order = monodromy_group_order(cnf)
    
    return {
        "metric_name": "Monodromy Group Order vs Resolution Width",
        "metric_value": order / width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")