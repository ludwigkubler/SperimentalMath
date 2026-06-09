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

def generate_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = [random.randint(1, n), -random.randint(1, n)]
        if random.choice([True, False]):
            clause[0] *= -1
        if random.choice([True, False]):
            clause[1] *= -1
        cnf.append(clause)
    return cnf

def dpll(cnf):
    def solve(assignment):
        unassigned = [var for var in range(1, n+1) if var not in assignment and -var not in assignment]
        if not unassigned:
            if all([any(lit in assignment for lit in clause) for clause in cnf]):
                return assignment
            else:
                return None
        var = unassigned[0]
        for val in [True, False]:
            new_assignment = assignment.copy()
            new_assignment[var] = val
            result = solve(new_assignment)
            if result is not None:
                return result
        return None

    n = max(abs(lit) for clause in cnf for lit in clause)
    return solve({})

def frege_proof_depth(cnf):
    def prove(assignment, clause):
        if not clause:
            return True
        var = abs(clause[0])
        if var in assignment and (assignment[var] == (clause[0] > 0)):
            return prove(assignment, [lit for lit in clause if lit != clause[0]])
        elif -var in assignment and (assignment[-var] == (clause[0] < 0)):
            return prove(assignment, [lit for lit in clause if lit != clause[0]])
        else:
            return False

    n = max(abs(lit) for clause in cnf for lit in clause)
    depth = 0
    for assignment in itertools.product([True, False], repeat=n):
        if all(prove(dict(zip(range(1, n+1), assignment)), clause) for clause in cnf):
            depth += 1
    return depth

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n, n * (n // 2))
        d = frege_proof_depth(cnf)
        R = len(dpll(cnf))  # Simplified representation size calculation
        results.append((R, d))
    
    if not results:
        return {
            "metric_name": "Frege Proof Depth vs. Representation Size",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    R_values = [R for R, _ in results]
    d_values = [d for _, d in results]
    
    mean_R = sum(R_values) / len(R_values)
    mean_d = sum(d_values) / len(d_values)
    var_R = sum((R - mean_R)**2 for R in R_values) / len(R_values)
    var_d = sum((d - mean_d)**2 for d in d_values) / len(d_values)
    cov_RD = sum((R - mean_R) * (d - mean_d) for R, d in results) / len(results)
    
    correlation_coefficient = cov_RD / math.sqrt(var_R * var_d)
    
    return {
        "metric_name": "Frege Proof Depth vs. Representation Size",
        "metric_value": correlation_coefficient,
        "instances_tested": len(R_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
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
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")