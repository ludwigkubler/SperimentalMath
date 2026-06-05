# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    q = 2 ** random.randint(3, 5)  # Finite field F_q with q = 2^k for k in [3, 5]
    n = random.choice([5, 10, 15, 20, 30, 40])  # Polynomial degree
    f = [random.randint(0, q - 1) for _ in range(n + 1)]  # Random polynomial coefficients
    
    # Construct Tseitin formula φ_f (simplified version)
    variables = {f"x{i}": i for i in range(n)}
    clauses = []
    for i in range(n):
        clauses.append((variables[f"x{i}"], f"~x{i+1}", "OR"))
        clauses.append((f"~x{i}", f"x{i+1}", "AND"))
    
    # Compute resolution proof width w(φ_f)
    def resolve(clauses, assignment):
        new_clauses = []
        for clause in clauses:
            if all(x in assignment and (assignment[x] == 0) for x in clause):
                continue
            new_clause = [x for x in clause if x not in assignment]
            if len(new_clause) > 1:
                new_clauses.append(new_clause)
        return new_clauses
    
    def is_satisfiable(clauses, assignment):
        while True:
            new_assignment = {}
            changed = False
            for clause in clauses:
                unsatisfied_vars = [x for x in clause if x not in assignment]
                if len(unsatisfied_vars) == 1:
                    new_assignment[unsatisfied_vars[0]] = 1 - assignment.get(clause[0], 0)
                    changed = True
            if not changed:
                break
        return any(all(x in assignment and (assignment[x] == 0) for x in clause) for clause in clauses)
    
    max_width = 0
    for _ in range(100):  # Sample 100 random assignments to estimate width
        assignment = {x: random.randint(0, 1) for x in variables}
        if is_satisfiable(clauses, assignment):
            width = len([var for var in assignment if var not in assignment])
            max_width = max(max_width, width)
    
    # Compute min_order(f) (simplified version)
    def min_order(f):
        return sum(1 for coeff in f if coeff != 0)
    
    min_order_f = min_order(f)
    
    # Correlation coefficient calculation
    if max_width == 0:
        correlation_coefficient = None
    else:
        correlation_coefficient = Fraction(min_order_f, max_width).limit_denominator()
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": float(correlation_coefficient) if correlation_coefficient is not None else None,
        "instances_tested": 100,
        "n_max": n,
        "conjecture_holds": correlation_coefficient is not None and correlation_coefficient >= Fraction(7, 10),
        "counterexample": "" if correlation_coefficient is not None else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.4f} std={sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values)/len(metric_values):.4f} support_fraction={support_fraction:.4f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")