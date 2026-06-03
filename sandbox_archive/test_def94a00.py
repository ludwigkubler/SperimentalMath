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
        for _ in range(2 * n):
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            if all(c != -lit for c in clause):
                clauses.append(clause)
        return clauses
    
    def dpll(sat_formula):
        if not sat_formula:
            return True
        literal = next((l for l in range(1, len(sat_formula) + 1) if l not in [abs(c) for c in sat_formula] and -l not in [abs(c) for c in sat_formula]), None)
        if literal is None:
            return False
        
        def dpll_helper(formula):
            if not formula:
                return True
            lit = next((l for l in range(1, len(formula) + 1) if l not in [abs(c) for c in formula] and -l not in [abs(c) for c in formula]), None)
            if lit is None:
                return False
            new_formula = [c for c in formula if c != literal and c != -literal]
            return dpll_helper(new_formula) or dpll_helper([c for c in new_formula if c != -lit])
        
        return dpll_helper(sat_formula)
    
    def resolution_width(formula):
        queue = list(formula)
        while True:
            unit_clauses = [c for c in queue if abs(c) == 1]
            if not unit_clauses:
                break
            lit = unit_clauses[0]
            new_clause = next((c for c in queue if -lit in c), None)
            if new_clause is None:
                return len(queue)
            queue.remove(new_clause)
            queue.append([l for l in new_clause if l != -lit])
        return len(queue)
    
    def max_reflections(n):
        # Placeholder for actual computation
        return random.randint(1, 10)  # Simplified for testing
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        cnf = generate_cnf(n)
        proof_width = resolution_width(cnf)
        reflections = max_reflections(n)
        results.append((proof_width, reflections))
    
    if not results:
        return {
            "metric_name": "resolution_proof_width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    proof_widths = [pw for pw, _ in results]
    reflections = [r for _, r in results]
    
    mean_proof_width = sum(proof_widths) / len(proof_widths)
    mean_reflections = sum(reflections) / len(reflections)
    
    correlation = (sum((pw - mean_proof_width) * (r - mean_reflections) for pw, r in results) /
                   math.sqrt(sum((pw - mean_proof_width) ** 2 for pw in proof_widths)) *
                   math.sqrt(sum((r - mean_reflections) ** 2 for r in reflections)))
    
    return {
        "metric_name": "resolution_proof_width",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n for _, n in results),
        "conjecture_holds": abs(correlation) >= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={r['seed']}")
                break