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

# Helper functions for generating Tseitin formulas and solving them with DPLL

def generate_tseitin_formula(n):
    literals = [f'x{i+1}' for i in range(n)]
    clauses = []
    
    # Generate clauses for the OR gate
    for i in range(1, n):
        clauses.append([literals[i-1], literals[i]])
    
    # Generate clauses for the AND gate
    for i in range(1, n):
        clauses.append([-literals[i-1], -literals[i]])
    
    # Add a clause to force one of the literals to be true
    clauses.append([literals[0]])
    
    return clauses, literals

def dpll(clauses, assignment):
    if not clauses:
        return True
    unit_clauses = [c for c in clauses if len(c) == 1]
    if unit_clauses:
        literal = unit_clauses[0][0]
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if dpll([c for c in clauses if literal not in c], new_assignment):
            return True
        new_assignment[literal] = False
        if dpll([c for c in clauses if -literal not in c], new_assignment):
            return True
        return False
    pure_literals = set()
    for clause in clauses:
        positive = [l for l in clause if l > 0]
        negative = [-l for l in clause if l < 0]
        if len(positive) == 1 and not any(-p in assignment for p in positive):
            pure_literals.add(positive[0])
        if len(negative) == 1 and not any(p in assignment for p in negative):
            pure_literals.add(negative[0])
    if pure_literals:
        literal = next(iter(pure_literals))
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if dpll([c for c in clauses if literal not in c], new_assignment):
            return True
        new_assignment[literal] = False
        if dpll([c for c in clauses if -literal not in c], new_assignment):
            return True
        return False
    literals = list(assignment.keys())
    literal = random.choice(literals)
    new_assignment = assignment.copy()
    new_assignment[literal] = True
    if dpll([c for c in clauses if literal not in c], new_assignment):
        return True
    new_assignment[literal] = False
    if dpll([c for c in clauses if -literal not in c], new_assignment):
        return True
    return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Test each n with 5 different instances
            clauses, literals = generate_tseitin_formula(n)
            assignment = {l: False for l in literals}
            resolution_refutation_size = 1 if dpll(clauses, assignment) else len(clauses)
            metric_values.append(math.log2(resolution_refutation_size))
            instances_tested += 1
    
    correlation_coefficient = 0
    mean_nu_G = sum(n_values) / len(n_values)
    for n in n_values:
        nu_G = n - 1
        y = math.log2(2**nu_G)
        correlation_coefficient += (n - mean_nu_G) * (math.log2(resolution_refutation_size) - y)
    correlation_coefficient /= (len(n_values) * sum((n - mean_nu_G)**2 for n in n_values))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "conjecture_holds": correlation_coefficient > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient\" first_failing_seed={first_failing_seed}")