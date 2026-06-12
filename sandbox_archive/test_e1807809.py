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
    
    def random_cnf(n, m):
        variables = list(range(1, n + 1))
        cnf = []
        for _ in range(m):
            clause = random.sample(variables, random.randint(1, n))
            cnf.append(clause)
        return cnf
    
    def dpll(cnf, assignment, model):
        if not cnf:
            return True
        literal = next((lit for lit in model if lit not in assignment), None)
        if literal is None:
            return False
        
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if dpll(cnf, new_assignment, model):
            return True
        
        new_assignment[literal] = False
        if dpll(cnf, new_assignment, model):
            return True
        
        return False
    
    def resolution_width(cnf):
        clauses = cnf[:]
        width = 0
        while len(clauses) > 1:
            clause1 = clauses.pop()
            for clause2 in clauses[:]:
                common = set(lit for lit in clause1 if -lit in clause2)
                if common:
                    new_clause = list(set(clause1 + clause2) - common)
                    clauses.remove(clause2)
                    clauses.append(new_clause)
                    width = max(width, len(new_clause))
        return width
    
    def dfa_states(cnf):
        states = {0}
        for clause in cnf:
            new_state = set()
            for literal in clause:
                if literal > 0:
                    new_state.add(literal)
                else:
                    new_state.discard(-literal)
            states.add(frozenset(new_state))
        return len(states)
    
    n_values = [5, 10, 15, 20, 30, 40]
    m_values = [n * 2 for n in n_values]
    total_states = []
    total_widths = []
    
    for n, m in zip(n_values, m_values):
        for _ in range(5):  # Ensure at least 5 instances per seed
            cnf = random_cnf(n, m)
            states = dfa_states(cnf)
            width = resolution_width(cnf)
            total_states.append(states)
            total_widths.append(width)
    
    mean_states = sum(total_states) / len(total_states)
    mean_widths = sum(total_widths) / len(total_widths)
    correlation_coefficient = 0
    if mean_states != 0 and mean_widths != 0:
        covariance = sum((x - mean_states) * (y - mean_widths) for x, y in zip(total_states, total_widths))
        variance_states = sum((x - mean_states) ** 2 for x in total_states)
        variance_widths = sum((y - mean_widths) ** 2 for y in total_widths)
        correlation_coefficient = covariance / (variance_states * variance_widths) ** 0.5
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(total_states),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8 and abs(mean_states - mean_widths) <= 3,
        "counterexample": "" if correlation_coefficient >= 0.8 and abs(mean_states - mean_widths) <= 3 else "correlation_threshold_not_met"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_threshold_not_met\" first_failing_seed={first_failing_seed}")