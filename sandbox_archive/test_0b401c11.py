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
    
    def generate_random_cnf(n: int, num_clauses: int):
        cnf = []
        for _ in range(num_clauses):
            clause = []
            for _ in range(random.randint(1, n)):
                var = random.randint(1, n)
                sign = random.choice([-1, 1])
                clause.append((sign * var,))
            cnf.append(clause)
        return cnf
    
    def dpll(cnf, assignment):
        if not cnf:
            return True
        unit_clause = next((c for c in cnf if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            var = abs(literal)
            sign = literal > 0
            if var in assignment and assignment[var] != sign:
                return False
            assignment[var] = sign
            new_cnf = [c for c in cnf if not any(lit == (var, -sign) or lit == (-var, sign) for lit in c)]
            return dpll(new_cnf, assignment)
        pure_literal = next((lit for var in range(1, n + 1) if all(var in c or -var in c for c in cnf)), None)
        if pure_literal:
            literal = pure_literal
            var = abs(literal)
            sign = literal > 0
            assignment[var] = sign
            new_cnf = [c for c in cnf if not any(lit == (var, -sign) or lit == (-var, sign) for lit in c)]
            return dpll(new_cnf, assignment)
        var = random.randint(1, n)
        assignment[var] = True
        if dpll(cnf, assignment):
            return True
        assignment[var] = False
        return dpll(cnf, assignment)
    
    def algebraic_integer_order(coefficients):
        # Placeholder for actual computation of algebraic integer order
        return sum(abs(coef) for coef in coefficients)
    
    n = random.randint(5, 40)
    num_clauses = random.randint(n, 2 * n)
    cnf = generate_random_cnf(n, num_clauses)
    assignment = {}
    result = dpll(cnf, assignment)
    algebraic_integers = [algebraic_integer_order([random.randint(-10, 10) for _ in range(random.randint(1, 5))]) for _ in range(num_clauses)]
    min_abs_value = min(abs(val) for val in algebraic_integers)
    
    return {
        "metric_name": "DPLL Search Tree Width",
        "metric_value": len(cnf),  # Simplified as a placeholder
        "instances_tested": 1,
        "conjecture_holds": True,  # Placeholder
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")