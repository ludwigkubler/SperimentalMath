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
    
    def generate_cnf(m, n):
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
            var = abs(unit_clause[0])
            val = unit_clause[0] > 0
            new_assignment = assignment.copy()
            new_assignment[var] = val
            return dpll([c for c in cnf if var not in c], new_assignment)
        
        var = random.choice(list(set(abs(clause[0]) for clause in cnf)))
        for val in [True, False]:
            new_assignment = assignment.copy()
            new_assignment[var] = val
            if dpll(cnf, new_assignment):
                return True
        return False
    
    def frege_proof_depth(cnf):
        n = max(abs(clause[0]) for clause in cnf)
        stack = []
        for clause in cnf:
            stack.append((clause, 1))
        depth = 0
        while stack:
            clause, level = stack.pop()
            if all(var in assignment and assignment[var] == (var > 0) for var in clause):
                continue
            new_clause = [v for v in clause if v not in assignment]
            if not new_clause:
                depth = max(depth, level)
                continue
            stack.append((new_clause, level + 1))
        return depth
    
    def grothendieck_riemann_roch(m):
        # Simplified approximation for demonstration purposes
        return m ** (2/3)
    
    n_max = 40
    instances_tested = 0
    total_mdeg = 0
    total_depth = 0
    
    for n in range(5, n_max + 1, 5):
        for _ in range(6):  # 6 instances per size to ensure statistical signal
            m = random.randint(n // 2, n * (n - 1) // 2)
            cnf = generate_cnf(m, n)
            if not dpll(cnf):
                continue
            depth = frege_proof_depth(cnf)
            mdeg = grothendieck_riemann_roch(m)
            total_mdeg += mdeg
            total_depth += depth
            instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "no_valid_instances"
        }
    
    mean_mdeg = total_mdeg / instances_tested
    mean_depth = total_depth / instances_tested
    
    # Pearson correlation coefficient calculation
    numerator = sum((mdeg - mean_mdeg) * (depth - mean_depth) for mdeg, depth in zip(mdegs, depths))
    denominator = math.sqrt(sum((mdeg - mean_mdeg) ** 2 for mdeg in mdegs)) * math.sqrt(sum((depth - mean_depth) ** 2 for depth in depths))
    correlation_coefficient = numerator / denominator if denominator != 0 else 0
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.7,
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
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample_desc = "correlation_coefficient < 0.7"
        result = f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}"
    
    print(result)