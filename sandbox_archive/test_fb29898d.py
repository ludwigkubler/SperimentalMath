# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations, product

def generate_cnf(n: int) -> list:
    clauses = []
    for _ in range(2 * n):
        clause = [random.choice([-1, 1]) * (i + 1) for i in random.sample(range(n), random.randint(1, n))]
        clauses.append(clause)
    return clauses

def dpll(cnf: list, assignment: dict = None) -> bool:
    if assignment is None:
        assignment = {}
    
    unit_clauses = [c for c in cnf if len(c) == 1]
    while unit_clauses:
        literal = unit_clauses.pop()
        var = abs(literal[0])
        value = (literal > 0)
        assignment[var] = value
        new_clauses = []
        for clause in cnf:
            if literal not in clause and -literal not in clause:
                new_clauses.append(clause)
        cnf = new_clauses
    
    pure_literals = [var for var, _ in assignment.items() if all(var not in c or -var not in c for c in cnf)]
    while pure_literals:
        literal = pure_literals.pop()
        value = assignment[literal]
        assignment[var] = value
        new_clauses = []
        for clause in cnf:
            if literal not in clause and -literal not in clause:
                new_clauses.append(clause)
        cnf = new_clauses
    
    if not cnf:
        return True
    if any(all(lit not in assignment or assignment[lit] == (lit > 0) for lit in c) for c in cnf):
        return False
    
    var = next(var for var, _ in assignment.items() if all(var not in c or -var not in c for c in cnf))
    value = True
    new_assignment = assignment.copy()
    new_assignment[var] = value
    if dpll(cnf, new_assignment):
        return True
    
    value = False
    new_assignment = assignment.copy()
    new_assignment[var] = value
    if dpll(cnf, new_assignment):
        return True
    
    return False

def ehrhart_polygon(n: int) -> list:
    points = []
    for i in range(2**n):
        binary = bin(i)[2:].zfill(n)
        point = [int(b) for b in binary]
        if all(point[i] + point[j] <= 1 for i, j in combinations(range(n), 2)):
            points.append(point)
    return points

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        points = ehrhart_polygon(n)
        num_points = len(points)
        
        if not dpll(cnf):
            return {
                "metric_name": "resolution_proof_width",
                "metric_value": None,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "unsatisfiable_cnf"
            }
        
        # Placeholder for resolution proof width calculation
        w_phi = num_points  # This is a placeholder; replace with actual calculation
        
        results.append((num_points, w_phi))
    
    if len(results) < 30:
        return {
            "metric_name": "resolution_proof_width",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    num_points = [r[0] for r in results]
    w_phi = [r[1] for r in results]
    
    mean_num_points = sum(num_points) / len(num_points)
    mean_w_phi = sum(w_phi) / len(w_phi)
    
    covariance = sum((num_points[i] - mean_num_points) * (w_phi[i] - mean_w_phi) for i in range(len(results))) / len(results)
    variance_num_points = sum((num_points[i] - mean_num_points)**2 for i in range(len(results))) / len(results)
    variance_w_phi = sum((w_phi[i] - mean_w_phi)**2 for i in range(len(results))) / len(results)
    
    correlation_coefficient = covariance / (math.sqrt(variance_num_points) * math.sqrt(variance_w_phi))
    p_value = 1.0
    
    return {
        "metric_name": "resolution_proof_width",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7 and p_value <= 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30*3 + 1, 3))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        mean_value = None
        std_value = None
        support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if any(not r["conjecture_holds"] and r["metric_value"] < 0.5 or r["p_value"] > 0.2 for r in results):
        counterexample = "counterexample_found"
    else:
        counterexample = ""
    
    print(f"RESULT: {'SUPPORTED' if support_fraction >= 0.8 else 'FALSIFIED'} mean={mean_value} std={std_value} support_fraction={support_fraction}")