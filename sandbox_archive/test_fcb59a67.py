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
            clause = [random.randint(-n, n) for _ in range(random.randint(1, 3))]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf):
        def solve(model):
            if not cnf:
                return True
            literal = next(lit for lit in range(1, len(model) + 1) if model[lit - 1] is None or model[lit - 1] == 0)
            pos_lit, neg_lit = literal, -literal
            if all(lit not in clause for clause in cnf):
                return solve(model[:literal - 1] + [pos_lit] + model[literal:])
            if any(all(-lit in clause for clause in cnf) for lit in (pos_lit, neg_lit)):
                return False
            model[literal - 1] = pos_lit
            if solve(model):
                return True
            model[literal - 1] = neg_lit
            if solve(model):
                return True
            model[literal - 1] = None
            return False
        
        return solve([None] * (max(abs(lit) for lit in sum(cnf, [])) + 1))
    
    def algebraic_variety(cnf):
        # Simplified version of finding irreducible polynomials
        # This is a placeholder and should be replaced with actual algebraic geometry code
        return len(cnf)
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        cnf = generate_cnf(n)
        d_phi = dpll(cnf)
        R_phi = algebraic_variety(cnf)
        
        if d_phi is None:
            continue
        
        metric_values.append(abs(R_phi - d_phi))
    
    if not metric_values:
        return {
            "metric_name": "Absolute Difference",
            "metric_value": 0.0,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    correlation_coefficient = sum((x - mean) * (y - mean) for x, y in zip(metric_values, range(len(metric_values)))) / len(metric_values)
    mean = sum(metric_values) / len(metric_values)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    
    return {
        "metric_name": "Absolute Difference",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": "" if abs(correlation_coefficient) >= 0.8 else f"Correlation coefficient below threshold"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds supported")