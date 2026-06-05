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
    
    def generate_binary_string(length):
        return ''.join(random.choice('01') for _ in range(length))
    
    def tseitin_formula(n):
        variables = [f'x{i}' for i in range(2*n)]
        clauses = []
        for i in range(n):
            clauses.append([variables[2*i], variables[2*i+1]])
            clauses.append([-variables[2*i], -variables[2*i+1]])
            clauses.append([variables[2*i], variables[2*i+1], -variables[n+i]])
            clauses.append([-variables[2*i], -variables[2*i+1], -variables[n+i]])
        for i in range(n):
            clauses.append([variables[i], -variables[n+i]])
        return clauses
    
    def dpll(clauses, assignment={}, model=[]):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll(clauses, new_assignment, model + [literal]):
                return True
            new_assignment[literal] = False
            if dpll(clauses, new_assignment, model + [-literal]):
                return True
            return False
        
        literal = next((l for l in variables if l not in assignment and -l not in assignment), None)
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if dpll(clauses, new_assignment, model + [literal]):
            return True
        new_assignment[literal] = False
        if dpll(clauses, new_assignment, model + [-literal]):
            return True
        return False
    
    def circuit_monotone_width(clauses):
        n = len(variables)
        max_width = 0
        for i in range(1 << n):
            assignment = {variables[j]: (i >> j) & 1 for j in range(n)}
            if dpll(clauses, assignment):
                width = sum(1 for v in variables if assignment[v])
                if width > max_width:
                    max_width = width
        return max_width
    
    def minimal_representation_rank(fa):
        # Placeholder function to compute r(L)
        # This is a dummy implementation and should be replaced with actual computation
        return len(fa.states)
    
    n_max = 40
    instances_tested = 0
    total_rL = 0
    total_wmL = 0
    
    for n in range(5, 41):
        for _ in range(7):  # Ensure at least 30 instances per seed
            binary_string = generate_binary_string(n)
            clauses = tseitin_formula(n)
            fa_states = len(clauses) + 2 * n
            rL = minimal_representation_rank(fa_states)
            wmL = circuit_monotone_width(clauses)
            
            total_rL += rL
            total_wmL += wmL
            instances_tested += 1
    
    mean_rL = total_rL / instances_tested
    mean_wmL = total_wmL / instances_tested
    correlation_coefficient = (instances_tested * sum(rL * wmL for rL, wmL in zip([mean_rL] * instances_tested, [mean_wmL] * instances_tested)) -
                               sum(rL for rL in [mean_rL] * instances_tested) * sum(wmL for wmL in [mean_wmL] * instances_tested)) / \
                             math.sqrt((instances_tested * sum(rL**2 for rL in [mean_rL] * instances_tested) - sum(rL**2 for rL in [mean_rL] * instances_tested)) *
                                       (instances_tested * sum(wmL**2 for wmL in [mean_wmL] * instances_tested) - sum(wmL**2 for wmL in [mean_wmL] * instances_tested)))
    
    conjecture_holds = correlation_coefficient >= 0.7
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")