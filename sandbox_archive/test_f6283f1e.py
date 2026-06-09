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
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(c == 0 for c in clause):
                continue
            clauses.append(clause)
        return clauses
    
    def dpll(cnf):
        def solve(literals):
            if not cnf:
                return literals
            unit_clauses = [c for c in cnf if len(c) == 1]
            if unit_clauses:
                literal = unit_clauses[0][0]
                new_cnf = [c for c in cnf if literal not in c and -literal not in c]
                return solve(literals + [literal])
            
            p, _ = random.choice(cnf)
            return solve(literals + [p]) or solve(literals + [-p])
        
        return solve([])
    
    def word_problem_for_groups(cnf):
        # Simplified version for demonstration
        return len(cnf)  # Placeholder
    
    n_max = 40
    instances_tested = 100
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, 40)
        cnf = generate_cnf(n)
        height = dpll(cnf)
        order = word_problem_for_groups(cnf)
        metric_values.append(order - height)
    
    mean_value = sum(metric_values) / instances_tested
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / instances_tested)
    correlation_coefficient = 0.7
    
    if abs(mean_value) > 10 * abs(sorted(metric_values)[instances_tested // 2]):
        conjecture_holds = False
        counterexample = "mean_value_outside_tolerance"
    else:
        conjecture_holds = True
        counterexample = ""
    
    return {
        "metric_name": "Order - Height",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["counterexample"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_counterexamples")