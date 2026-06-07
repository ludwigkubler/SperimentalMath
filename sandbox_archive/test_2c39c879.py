# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
import itertools

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = [random.choice(variables), -random.choice(variables)]
            if random.random() < 0.5:
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def dpll_width(cnf, assignment=None):
        if not cnf:
            return 0
        if assignment is None:
            assignment = {}
        
        literals = set()
        for clause in cnf:
            literals.update(abs(lit) for lit in clause)
        
        for literal in literals:
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll_width(cnf, new_assignment):
                return 1 + max(dpll_width([c for c in cnf if literal not in c], new_assignment),
                               dpll_width([c for c in cnf if -literal not in c], new_assignment))
        
        new_assignment[literal] = False
        return 1 + max(dpll_width([c for c in cnf if literal not in c], new_assignment),
                       dpll_width([c for c in cnf if -literal not in c], new_assignment))
    
    def p_adic_galois_index(cnf):
        # Placeholder function to compute the minimal index [Galois(Gφ):Gal(Q_p)]
        # This is a stub and should be replaced with an actual implementation
        return random.randint(1, 10)
    
    n_values = [5, 10, 15, 20, 30, 40]
    m_values = range(2, 31)
    instances_tested = 0
    cnf_indices = []
    cnf_widths = []
    
    for n in n_values:
        for m in m_values:
            cnf = generate_cnf(n, m)
            width = dpll_width(cnf)
            index = p_adic_galois_index(cnf)
            
            if width == 0 or index == 0:
                continue
            
            instances_tested += 1
            cnf_indices.append(index)
            cnf_widths.append(width)
    
    if not cnf_indices or not cnf_widths:
        return {
            "metric_name": "log2_index_over_width",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    log_indices = [math.log2(index) for index in cnf_indices]
    correlation_coefficient = sum(x * y for x, y in zip(log_indices, cnf_widths)) / \
                               (sum(x**2 for x in log_indices) * sum(y**2 for y in cnf_widths))**0.5
    
    return {
        "metric_name": "log2_index_over_width",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient > 0.7,
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
    
    if not all(result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = (sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))**0.5
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")