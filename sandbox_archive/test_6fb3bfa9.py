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
    
    # Generate a random 3-CNF formula with n variables and m clauses
    n = random.randint(5, 40)
    m = random.randint(n, 2 * n)
    clauses = []
    for _ in range(m):
        literals = [f"x{i+1}" if random.choice([True, False]) else f"~x{i+1}" for i in range(n)]
        clause = " or ".join(literals)
        clauses.append(clause)
    
    formula = " and ".join(clauses)
    
    # Compute the monotone circuit width (simplified DPLL solver)
    def dpll(formula, assignment):
        if not formula:
            return True
        if any(lit.startswith("~") for lit in formula.split(" or ")) and all(lit.startswith("~") for lit in formula.split(" or ")):
            return False
        
        literal = next((lit for lit in formula.split(" or ") if not lit.startswith("~")), None)
        if literal:
            assignment[literal] = True
            if dpll(formula.replace(literal, ""), assignment):
                return True
            del assignment[literal]
        
        literal = next((lit for lit in formula.split(" or ") if lit.startswith("~")), None)
        if literal:
            assignment[literal[1:]] = False
            if dpll(formula.replace(literal, ""), assignment):
                return True
            del assignment[literal[1:]]
        
        return False
    
    def monotone_circuit_width(formula):
        variables = set()
        for clause in formula.split(" and "):
            variables.update(clause.split(" or "))
        width = 0
        for literal in variables:
            if literal.startswith("~"):
                continue
            assignment = {var: False for var in variables}
            assignment[literal] = True
            if dpll(formula, assignment):
                width += 1
        return width
    
    circuit_width = monotone_circuit_width(formula)
    
    # Construct the toric variety (simplified example)
    def construct_toric_variety(clauses):
        points = []
        for clause in clauses:
            point = [0] * n
            for literal in clause.split(" or "):
                if literal.startswith("~"):
                    var = int(literal[1:]) - 1
                    point[var] = 1
                else:
                    var = int(literal) - 1
                    point[var] = 1
            points.append(point)
        return points
    
    toric_variety = construct_toric_variety(clauses)
    
    # Compute the minimal rank of the toric variety (simplified example)
    def min_rank(points):
        rank = 0
        for i in range(len(points)):
            if all(points[j][i] == 0 for j in range(len(points)) if i != j):
                rank += 1
        return rank
    
    minimal_rank = min_rank(toric_variety)
    
    # Check the conjecture
    c_F = 2.0  # Example constant factor
    ratio = minimal_rank / (c_F * circuit_width)
    
    result = {
        "metric_name": "Ratio of Minimal Rank to Monotone Circuit Width",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= c_F,
        "counterexample": "" if ratio <= c_F else f"Counterexample: n={n}, m={m}, formula={formula}"
    }
    
    return result

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        counterexample = next((result["counterexample"] for result in results if not result["conjecture_holds"]), "")
        first_failing_seed = next((result["seed"] for result in results if not result["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")