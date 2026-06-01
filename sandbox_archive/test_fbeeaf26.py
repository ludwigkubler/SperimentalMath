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
        for _ in range(10 * n):  # Generate 10n clauses to ensure variety
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf, assignment):
        if not cnf:
            return True
        for literal in cnf[0]:
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
                return True
        return False
    
    def lefschetz_fitting_ideal(cnf):
        # Simplified version of Lefschetz Fitting Ideal calculation
        # This is a placeholder; actual implementation depends on the specific conjecture
        return len(cnf)
    
    n = 10  # Start with small n and increase
    instances_tested = 0
    total_generators = 0
    total_diameter = 0
    
    while n <= 40:
        cnf = generate_cnf(n)
        generators = lefschetz_fitting_ideal(cnf)
        diameter = dpll(cnf, {})
        
        if generators > 0 and diameter is not None:
            instances_tested += 1
            total_generators += generators
            total_diameter += diameter
        
        n += 5
    
    if instances_tested < 30:
        return {
            "metric_name": "correlation",
            "metric_value": float('nan'),
            "instances_tested": instances_tested,
            "n_max": n - 5,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_generators = total_generators / instances_tested
    mean_diameter = total_diameter / instances_tested
    
    correlation_coefficient = (instances_tested * sum(g * d for g, d in zip(total_generators, total_diameter)) -
                                total_generators * total_diameter) / \
                               math.sqrt((instances_tested * sum(g**2 for g in total_generators) - total_generators**2) *
                                         (instances_tested * sum(d**2 for d in total_diameter) - total_diameter**2))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n - 5,
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and abs(mean_generators - mean_diameter) <= 3,
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
    
    mean_value = sum(r["metric_value"] for r in results if not math.isnan(r["metric_value"])) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results if not math.isnan(r["metric_value"])) /
                 len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE insufficient_support_fraction")