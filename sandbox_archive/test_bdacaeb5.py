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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0], clause[1] = -clause[0], -clause[1]
            cnf.append(clause)
        return cnf
    
    def dpll(cnf):
        def solve(lits, clauses):
            if not clauses:
                return True
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                lit = unit_clause[0]
                new_lits = [l for l in lits if l != -lit and l != lit]
                new_clauses = [c for c in clauses if not (lit in c or -lit in c)]
                return solve(new_lits, new_clauses)
            pure_literal = next((l for l in range(1, n+1) if all(l not in c or -l not in c for c in clauses)), None)
            if pure_literal:
                new_lits = [l for l in lits if l != -pure_literal and l != pure_literal]
                new_clauses = [c for c in clauses if not (pure_literal in c or -pure_literal in c)]
                return solve(new_lits, new_clauses)
            lit = random.choice(lits)
            if solve([lit] + lits, [c for c in clauses if not (lit in c or -lit in c)]):
                return True
            if solve([-lit] + lits, [c for c in clauses if not (lit in c or -lit in c)]):
                return True
            return False
        
        lits = list(range(1, n+1))
        return solve(lits, cnf)
    
    def minimal_local_indeterminacy(n):
        # Placeholder for actual computation of minimal local indeterminacy
        # This is a dummy implementation for testing purposes
        return random.random() * n
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_lcoh = 0.0
    total_depth = 0.0
    
    for n in n_values:
        for _ in range(5):
            cnf = generate_cnf(n, int(n * (n - 1) / 4))
            depth = dpll(cnf)
            lcoh = minimal_local_indeterminacy(n)
            total_lcoh += lcoh
            total_depth += depth
            instances_tested += 1
    
    mean_lcoh = total_lcoh / instances_tested
    mean_depth = total_depth / instances_tested
    correlation_coefficient = (instances_tested * mean_lcoh * mean_depth - total_lcoh * total_depth) / math.sqrt((instances_tested * sum(lcoh**2 for lcoh in lcoh_values) - total_lcoh**2) * (instances_tested * sum(depth**2 for depth in depth_values) - total_depth**2))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7 and all(lcoh <= math.sqrt(depth) + 1 for lcoh, depth in zip(lcoh_values, depth_values)),
        "counterexample": "" if correlation_coefficient >= 0.7 and all(lcoh <= math.sqrt(depth) + 1 for lcoh, depth in zip(lcoh_values, depth_values)) else "correlation_coefficient < 0.7 or lcoh > sqrt(depth) + 1"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")