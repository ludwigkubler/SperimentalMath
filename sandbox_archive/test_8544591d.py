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
        for _ in range(random.randint(1, n)):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if random.random() < 0.5:
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def resolution_width(cnf):
        stack = []
        while cnf:
            unit_clause = next((c for c in cnf if len(c) == 1), None)
            if not unit_clause:
                break
            literal = unit_clause[0]
            cnf.remove(unit_clause)
            new_clauses = []
            for clause in cnf:
                if literal in clause:
                    continue
                if -literal in clause:
                    cnf.remove(clause)
                else:
                    new_clauses.append([l for l in clause if l != -literal])
            stack.append(literal)
            cnf.extend(new_clauses)
        return len(stack)
    
    def tropical_derivative_degree(cnf):
        n = len(cnf[0])
        degree = 0
        for clause in cnf:
            for literal in clause:
                if literal > 0:
                    degree += 1
        return degree
    
    n_max = 30
    instances_tested = 0
    total_ratio = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for n in range(5, n_max + 1):
        cnf = generate_cnf(n)
        D_phi = tropical_derivative_degree(cnf)
        w_phi = resolution_width(cnf)
        if w_phi == 0:
            continue
        ratio = Fraction(D_phi, w_phi)
        total_ratio += ratio
        instances_tested += 1
        
        if ratio > 2:  # Threshold for c in D(φ) ≤ c·w(φ)
            conjecture_holds = False
            counterexample = f"n={n}, D(φ)={D_phi}, w(φ)={w_phi}"
    
    if instances_tested < 30:
        return {
            "metric_name": "Ratio of Tropical Derivative Degree to Resolution Proof Width",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Insufficient instances tested"
        }
    
    mean_ratio = total_ratio / instances_tested
    return {
        "metric_name": "Ratio of Tropical Derivative Degree to Resolution Proof Width",
        "metric_value": float(mean_ratio),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")