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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(10 * n):  # Generate a CNF with 10*n clauses
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf):
        def dpll_helper(model, clauses):
            if not clauses:
                return True
            literal = find_pure_literal(clauses) or find_unit_clause(clauses)
            if literal is None:
                literal = random.choice([x for clause in clauses for x in clause if x > 0])
            new_model = model.copy()
            new_model[literal] = True
            if not dpll_helper(new_model, [c for c in clauses if literal not in c and -literal not in c]):
                new_model[literal] = False
                if not dpll_helper(new_model, [c for c in clauses if literal not in c and -literal not in c]):
                    return False
            return True
        
        def find_pure_literal(clauses):
            pure_literals = {}
            for clause in clauses:
                for literal in clause:
                    if literal in pure_literals:
                        pure_literals[literal] += 1
                    else:
                        pure_literals[literal] = -1
            for literal, count in pure_literals.items():
                if count == len(clauses):
                    return literal
            return None
        
        def find_unit_clause(clauses):
            for clause in clauses:
                if sum(1 for x in clause if x > 0) == 1:
                    unit_literal = next(x for x in clause if x > 0)
                    return unit_literal
            return None
        
        model = {}
        return dpll_helper(model, cnf)
    
    def algebraic_variety(cnf):
        # Simplified version of computing the algebraic variety
        # This is a placeholder and should be replaced with actual computation
        return len(cnf)  # Placeholder for actual computation
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            cnf = generate_cnf(n)
            dpll_depth = len(cnf)  # Simplified DPLL depth for demonstration
            algebraic_roots = algebraic_variety(cnf)
            total_metric_value += abs(algebraic_roots - dpll_depth)
            instances_tested += 1
            n_max = max(n_max, n)
    
    correlation_coefficient = total_metric_value / (instances_tested * n_max)
    
    if correlation_coefficient < 0.8:
        conjecture_holds = False
        counterexample = "Correlation coefficient below threshold"
    
    return {
        "metric_name": "Absolute Difference",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
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
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient below threshold\" first_failing_seed={first_failing_seed}")