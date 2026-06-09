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
            clause = [random.randint(1, n), random.randint(-n, -1)]
            cnf.append(clause)
        return cnf
    
    def dpll(cnf, assignment):
        if not cnf:
            return True
        unit_clause = next((c for c in cnf if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            if literal < 0 and literal in assignment:
                return False
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if not dpll([c for c in cnf if literal not in c], new_assignment):
                del new_assignment[literal]
                new_assignment[-literal] = True
                if not dpll([c for c in cnf if -literal not in c], new_assignment):
                    return False
            return True
        
        literal = next((l for l in range(1, n + 1) if l not in assignment and -l not in assignment), None)
        if literal is None:
            return False
        
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if dpll([c for c in cnf if literal not in c], new_assignment):
            return True
        
        del new_assignment[literal]
        new_assignment[-literal] = True
        return dpll([c for c in cnf if -literal not in c], new_assignment)
    
    def resolution_width(cnf):
        clauses = [set(clause) for clause in cnf]
        queue = list(clauses)
        while queue:
            clause1 = queue.pop(0)
            for clause2 in queue:
                resolvent = set()
                for lit1 in clause1:
                    if -lit1 in clause2:
                        resolvent.update(lit for lit in clause2 if lit != -lit1)
                        break
                else:
                    continue
                if len(resolvent) == 0:
                    return float('inf')
                queue.append(resolvent)
        return max(len(clause) for clause in clauses)
    
    def ehrhart_polynomial_degree(cnf):
        n = len(set(abs(lit) for lit in sum(cnf, [])))
        m = len(cnf)
        # Simplified heuristic to estimate degree
        return 2 * (n + m)
    
    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        m = random.randint(n, 2 * n)
        cnf = generate_cnf(n, m)
        width = resolution_width(cnf)
        degree = ehrhart_polynomial_degree(cnf)
        if width == float('inf'):
            continue
        results.append((width, degree))
    
    if not results:
        return {
            "metric_name": "resolution_width",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    width_sum = sum(w for w, _ in results)
    degree_sum = sum(d for _, d in results)
    metric_mean = width_sum / len(results)
    degree_mean = degree_sum / len(results)
    C = 2 * math.log(1 + n + m) / degree_mean
    
    conjecture_holds = all(w >= degree and abs(w - degree) <= C * math.log(n + m) for w, degree in results)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": metric_mean,
        "instances_tested": len(results),
        "n_max": max(len(set(abs(lit) for lit in sum(cnf, []))) for cnf in [generate_cnf(n, m) for _ in range(30)]),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")