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
    
    def dfa_states(cnf):
        states = {0}
        for clause in cnf:
            new_states = set()
            for state in states:
                if all(abs(lit) not in state for lit in clause):
                    new_state = tuple(sorted(state + [abs(lit)]))
                    new_states.add(new_state)
            states.update(new_states)
        return len(states)
    
    def resolution_width(cnf):
        clauses = set(tuple(clause) for clause in cnf)
        width = 0
        while True:
            new_clauses = set()
            for clause1 in clauses:
                for clause2 in clauses:
                    if any(abs(lit) not in clause1 and abs(lit) not in clause2 for lit in clause1):
                        new_clause = tuple(sorted(set(clause1 + clause2) - {0}))
                        if len(new_clause) > width:
                            width = len(new_clause)
                        new_clauses.add(new_clause)
            if not new_clauses:
                break
            clauses.update(new_clauses)
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        m_phi = dfa_states(cnf)
        w_phi = resolution_width(cnf)
        
        results.append({
            "n": n,
            "m_phi": m_phi,
            "w_phi": w_phi
        })
    
    correlation_coefficient = 0
    mean_mte = sum(result["m_phi"] for result in results) / len(results)
    mean_wte = sum(result["w_phi"] for result in results) / len(results)
    
    for result in results:
        correlation_coefficient += (result["m_phi"] - mean_mte) * (result["w_phi"] - mean_wte)
    correlation_coefficient /= len(results)
    
    mean_absolute_difference = sum(abs(result["m_phi"] - result["w_phi"]) for result in results) / len(results)
    
    conjecture_holds = correlation_coefficient >= 0.8 and mean_absolute_difference <= 3
    counterexample = "correlation_threshold_not_met" if not conjecture_holds else ""
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")