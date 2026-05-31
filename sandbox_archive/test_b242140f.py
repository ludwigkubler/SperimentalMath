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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def is_satisfiable(cnf):
        stack = []
        assignment = {}
        
        def dfs(i):
            if i == len(cnf) + 1:
                return True
            for literal in cnf[i-1]:
                var = abs(literal)
                sign = literal > 0
                if var not in assignment:
                    assignment[var] = sign
                    stack.append((var, not sign))
                    if dfs(i+1):
                        return True
                    del assignment[var]
                    stack.pop()
                elif assignment[var] == sign:
                    continue
                else:
                    while stack and stack[-1][0] != var:
                        stack.pop()
                    if stack:
                        _, negated = stack.pop()
                        assignment[var] = not negated
                        if dfs(i):
                            return True
                        del assignment[var]
            return False
        
        return dfs(1)
    
    def resolution_width(cnf):
        clauses = cnf[:]
        width = 0
        while True:
            new_clauses = []
            for i in range(len(clauses)):
                for j in range(i+1, len(clauses)):
                    if any(-lit in clauses[j] for lit in clauses[i]):
                        new_clause = [lit for lit in clauses[i] if lit not in [-x for x in clauses[j]]]
                        new_clause.extend([lit for lit in clauses[j] if lit not in [-x for x in clauses[i]]])
                        new_clauses.append(new_clause)
            if not new_clauses:
                break
            width += 1
            clauses.extend(new_clauses)
        return width
    
    def hyperbolic_surface(cnf):
        n = len(cnf[0])
        automorphisms = set()
        for perm in itertools.permutations(range(1, n+1)):
            if all(abs(lit) == abs(perm[lit-1]) and lit * perm[lit-1] > 0 for lit in range(1, n+1)):
                automorphisms.add(tuple(perm))
        return len(automorphisms)
    
    instances_tested = 0
    m_phi_values = []
    w_phi_values = []
    n_max = 5
    
    for _ in range(30):
        n = random.randint(5, 40)
        cnf = generate_cnf(n)
        if not is_satisfiable(cnf):
            continue
        
        instances_tested += 1
        m_phi = hyperbolic_surface(cnf)
        w_phi = resolution_width(cnf)
        
        m_phi_values.append(m_phi)
        w_phi_values.append(w_phi)
        
        n_max = max(n_max, n)
    
    if instances_tested < 30:
        return {
            "metric_name": "m_phi vs w_phi",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_m_phi = sum(m_phi_values) / len(m_phi_values)
    mean_w_phi = sum(w_phi_values) / len(w_phi_values)
    covariance = sum((m_phi - mean_m_phi) * (w_phi - mean_w_phi) for m_phi, w_phi in zip(m_phi_values, w_phi_values)) / len(m_phi_values)
    variance_m_phi = sum((m_phi - mean_m_phi)**2 for m_phi in m_phi_values) / len(m_phi_values)
    variance_w_phi = sum((w_phi - mean_w_phi)**2 for w_phi in w_phi_values) / len(w_phi_values)
    
    pearson_corr_coeff = covariance / (variance_m_phi * variance_w_phi**0.5)
    
    return {
        "metric_name": "m_phi vs w_phi",
        "metric_value": pearson_corr_coeff,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": pearson_corr_coeff >= 0.7 and pearson_corr_coeff <= -0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r['metric_value'] for r in results if r['metric_value'] is not None) / len(results)
    std_metric_value = (sum((r['metric_value'] - mean_metric_value)**2 for r in results if r['metric_value'] is not None) / len(results))**0.5
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")