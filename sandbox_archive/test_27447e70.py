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

def generate_tseitin_formula(n, m):
    variables = [f'x{i}' for i in range(1, n+1)]
    clauses = []
    
    # Generate literals
    literals = [random.choice(variables) if random.choice([True, False]) else f'~{v}' for v in variables]
    
    # Generate clauses
    for _ in range(m):
        clause = random.sample(literals, 2)
        clauses.append(f"({clause[0]} OR {clause[1]})")
    
    return literals, clauses

def construct_diophantine_equations(variables, clauses):
    equations = []
    for clause in clauses:
        if 'OR' in clause:
            lhs, rhs = clause.split(' OR ')
            equations.append(f"{lhs} + {rhs} >= 2")
            equations.append(f"{lhs} - {rhs} <= 1")
            equations.append(f"{rhs} - {lhs} <= 1")
        else:
            equations.append(clause)
    return equations

def solve_diophantine_equations(equations):
    # Simplify the system of Diophantine equations
    num_solutions = 0
    for equation in equations:
        if 'OR' not in equation:
            continue
        lhs, rhs = equation.split(' OR ')
        if int(lhs) + int(rhs) >= 2 and abs(int(lhs) - int(rhs)) <= 1:
            num_solutions += 1
    return num_solutions

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_max = 40
    instances_tested = 0
    total_metric_value = 0
    
    for n in range(5, n_max + 1):
        m = random.randint(n, 2*n)
        literals, clauses = generate_tseitin_formula(n, m)
        equations = construct_diophantine_equations(literals, clauses)
        
        num_solutions = solve_diophantine_equations(equations)
        resolution_proof_width = len(clauses) + n - 1
        
        instances_tested += 1
        total_metric_value += abs(num_solutions - resolution_proof_width)
    
    metric_value = total_metric_value / instances_tested
    conjecture_holds = all(abs(num_solutions - resolution_proof_width) <= 2 * resolution_proof_width for _, m, literals, clauses in trials)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "abs_diff",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unsupported_conjecture")