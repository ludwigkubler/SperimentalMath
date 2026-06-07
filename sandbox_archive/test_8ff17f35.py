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
        for _ in range(2**n):
            clause = [random.randint(-1, n) for _ in range(random.randint(1, n))]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def resolution_width(cnf):
        # Simplified DPLL solver to estimate width
        queue = cnf[:]
        learned_clauses = []
        while queue:
            literal = next((l for l in queue if l > 0), None)
            if not literal:
                break
            queue.remove(literal)
            learned_clauses.append([-literal])
            for clause in cnf:
                if literal in clause:
                    clause.remove(literal)
                if -literal in clause:
                    clause.remove(-literal)
                    if not clause:
                        return 0
        return max(len(clause) for clause in learned_clauses)
    
    def theta_min(cnf):
        # Simplified mapping to estimate minimal rank
        n = len(set(abs(lit) for lit in cnf[0]))
        return Fraction(n, 2)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n)
            theta_val = theta_min(cnf)
            width = resolution_width(cnf)
            results.append((theta_val, width))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    theta_vals, widths = zip(*results)
    mean_theta = sum(theta_vals) / len(theta_vals)
    mean_width = sum(widths) / len(widths)
    correlation_coefficient = (sum((theta - mean_theta) * (width - mean_width) for theta, width in results) /
                               math.sqrt(sum((theta - mean_theta)**2 for theta in theta_vals) *
                                         sum((width - mean_width)**2 for width in widths)))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for n, _ in results),
        "conjecture_holds": correlation_coefficient >= 0.95,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 10**6) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        outcome = "SUPPORTED"
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        mean_value = None
        support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
        outcome = "FALSIFIED"
    
    print(f"RESULT: {outcome} mean={mean_value} std=None support_fraction={support_fraction}")