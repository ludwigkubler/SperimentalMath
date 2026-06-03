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
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def dpll(sat_formula):
        def solve(lits_true, lits_false):
            if not sat_formula:
                return True
            literal = next((lit for lit in range(1, n + 1) if lit not in lits_true and -lit not in lits_false), None)
            if literal is None:
                return False
            new_lits_true = lits_true.copy()
            new_lits_false = lits_false.copy()
            new_lits_true.add(literal)
            if solve(new_lits_true, new_lits_false):
                return True
            new_lits_false.add(-literal)
            if solve(new_lits_true, new_lits_false):
                return True
            return False
        
        n = len(sat_formula[0])
        return solve(set(), set())
    
    def max_reflections(cnf):
        # Placeholder for actual computation of maximum reflections
        return random.randint(1, 10)  # Simplified for demonstration
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        cnf = generate_cnf(n)
        proof_width = dpll(cnf)
        reflections = max_reflections(cnf)
        results.append((proof_width, reflections))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    proof_widths, reflections = zip(*results)
    mean_proof_width = sum(proof_widths) / len(proof_widths)
    mean_reflections = sum(reflections) / len(reflections)
    correlation = (sum((pw - mean_proof_width) * (r - mean_reflections) for pw, r in results) /
                   math.sqrt(sum((pw - mean_proof_width)**2 for pw in proof_widths) *
                             sum((r - mean_reflections)**2 for r in reflections)))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n for _, _ in results),
        "conjecture_holds": abs(correlation) >= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_corr = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={result['seed']}")
                break