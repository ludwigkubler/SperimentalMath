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
        cnf = []
        for i in range(1, n+1):
            clause = [random.randint(1, 2*n) for _ in range(3)]
            cnf.append(clause)
        return cnf
    
    def is_satisfiable(cnf):
        n = len(cnf)
        assignment = [False] * (2 * n + 1)
        
        def dfs(i):
            if i > n:
                return True
            for literal in cnf[i-1]:
                var = abs(literal)
                if literal > 0 and not assignment[var]:
                    assignment[var] = True
                    if dfs(i+1):
                        return True
                    assignment[var] = False
                elif literal < 0 and assignment[-literal]:
                    assignment[-literal] = False
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
                        new_clause = [lit for lit in clauses[i] + clauses[j] if lit not in [-x for x in clauses[i]] and lit not in [-x for x in clauses[j]]]
                        width = max(width, len(new_clause))
                        new_clauses.append(new_clause)
            if not new_clauses:
                break
            clauses.extend(new_clauses)
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    m_phi_values = []
    w_values = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        if is_satisfiable(cnf):
            m_phi = len(generate_hyperbolic_surface(cnf))
            w = resolution_width(cnf)
            m_phi_values.append(m_phi)
            w_values.append(w)
    
    if not m_phi_values or not w_values:
        return {
            "metric_name": "m_phi vs. w",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "unsatisfiable_cnf"
        }
    
    def generate_hyperbolic_surface(cnf):
        # Placeholder for the actual hyperbolic surface generation logic
        return [random.randint(1, 10) for _ in range(len(cnf))]
    
    m_phi_mean = sum(m_phi_values) / len(m_phi_values)
    w_mean = sum(w_values) / len(w_values)
    correlation_coefficient = (sum((m_phi - m_phi_mean) * (w - w_mean) for m_phi, w in zip(m_phi_values, w_values)) /
                               math.sqrt(sum((m_phi - m_phi_mean)**2 for m_phi in m_phi_values) *
                                         sum((w - w_mean)**2 for w in w_values)))
    
    return {
        "metric_name": "m_phi vs. w",
        "metric_value": correlation_coefficient,
        "instances_tested": len(m_phi_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_C = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_C = math.sqrt(sum((r["metric_value"] - mean_C)**2 for r in results if r["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_C} std={std_C} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unsupported_metric")