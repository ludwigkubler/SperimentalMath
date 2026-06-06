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
from itertools import combinations, permutations

def generate_sat_instance(n: int) -> list:
    variables = [f'x{i}' for i in range(1, n+1)]
    clauses = []
    for k in range(2, n+1):
        for combo in combinations(variables, k):
            clause = ' or '.join(combo)
            clauses.append(f'not ({clause})')
    return clauses

def indicator_polynomial(cnf: list) -> list:
    poly = [0] * (len(cnf) + 1)
    for i, clause in enumerate(cnf):
        if 'or' not in clause:
            continue
        terms = clause.split(' or ')
        for term in terms:
            if 'not' in term:
                var = term[4:]
                poly[i+1] += -1
            else:
                var = term
                poly[i+1] += 1
    return poly

def tropical_abelianization(poly: list) -> int:
    n = len(poly)
    abelianization = 0
    for i in range(n):
        if poly[i] != 0:
            abelianization += abs(poly[i])
    return abelianization

def dpll(cnf: list, assignment: dict = None) -> bool:
    if assignment is None:
        assignment = {}
    if len(cnf) == 0:
        return True
    for clause in cnf:
        if 'or' not in clause:
            continue
        terms = clause.split(' or ')
        satisfied = False
        for term in terms:
            if 'not' in term:
                var = term[4:]
                if var not in assignment or not assignment[var]:
                    satisfied = True
                    break
            else:
                var = term
                if var in assignment and assignment[var]:
                    satisfied = True
                    break
        if satisfied:
            continue
        for var in variables:
            if var not in assignment:
                new_assignment = assignment.copy()
                new_assignment[var] = True
                if dpll(cnf, new_assignment):
                    return True
                new_assignment[var] = False
                if dpll(cnf, new_assignment):
                    return True
        return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 0
    total_ab = 0
    total_dlpl = 0
    for n in range(5, 41):
        cnf = generate_sat_instance(n)
        poly = indicator_polynomial(cnf)
        abelianization = tropical_abelianization(poly)
        dlpl_length = len(dpll(cnf))
        if abelianization == 0 or dlpl_length == 0:
            continue
        total_ab += abelianization
        total_dlpl += dlpl_length
        instances_tested += 1
    if instances_tested < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    correlation_coefficient = total_ab / total_dlpl
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={first_failing_seed}")