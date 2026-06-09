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
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        p = next((p for p in range(1, len(cnf) + 1) if p not in assignment and -p not in assignment), None)
        if p is None:
            return False
        if dpll(substitute(cnf, p, True), assignment | {p: True}):
            return True
        if dpll(substitute(cnf, p, False), assignment | {p: False}):
            return True
        return False
    
    def substitute(cnf, p, value):
        new_cnf = []
        for clause in cnf:
            if any(abs(lit) == abs(p) for lit in clause):
                continue
            new_clause = [lit for lit in clause if lit != -p]
            if not new_clause:
                return None
            new_cnf.append(new_clause)
        return new_cnf
    
    def topological_entropy(cnf, max_n=100):
        if len(cnf) > max_n:
            return float('inf')
        transitions = {}
        for _ in range(1000):  # Simulate 1000 random assignments
            assignment = {p: random.choice([True, False]) for p in range(1, len(cnf) + 1)}
            if dpll(cnf, assignment):
                continue
            for lit in cnf:
                if any(abs(l) == abs(p) for l in lit):
                    continue
                new_assignment = assignment.copy()
                new_assignment[p] = True
                if dpll(substitute(cnf, p, True), new_assignment):
                    transitions[(tuple(sorted(assignment.items())), True)] = (tuple(sorted(new_assignment.items())), False)
        return math.log(len(transitions)) / len(cnf)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    entropy = topological_entropy(cnf)
    
    if entropy == float('inf'):
        return {
            "metric_name": "topological_entropy",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "max_n_exceeded"
        }
    
    C = 2.0  # Example constant
    upper_bound = C * math.log(n)
    
    return {
        "metric_name": "topological_entropy",
        "metric_value": entropy,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(entropy - upper_bound) <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(abs(result["metric_value"] - (C * math.log(result["n_max"]))) > 3 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if abs(result["metric_value"] - (C * math.log(result["n_max"]))) > 3)
        print(f"RESULT: FALSIFIED counterexample=\"exceeds_bound\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")