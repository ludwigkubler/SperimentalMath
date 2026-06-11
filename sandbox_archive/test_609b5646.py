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

def generate_cnf(m, n):
    cnf = []
    for _ in range(m):
        clause = [random.randint(1, n), -random.randint(1, n)]
        while len(set(clause)) != 2:
            clause = [random.randint(1, n), -random.randint(1, n)]
        cnf.append(tuple(sorted(clause)))
    return tuple(cnf)

def resolution(cnf):
    clauses = list(cnf)
    new_clauses = set()
    while True:
        added = False
        for i in range(len(clauses)):
            for j in range(i + 1, len(clauses)):
                common_lits = set(x for x in clauses[i] if -x in clauses[j])
                if common_lits:
                    new_clause = tuple(sorted([l for l in clauses[i] + clauses[j] if l not in common_lits]))
                    if new_clause not in new_clauses and new_clause not in clauses:
                        new_clauses.add(new_clause)
                        added = True
        if not added:
            break
        clauses.extend(new_clauses)
        new_clauses.clear()
    return len(clauses)

def geometric_group_action(cnf):
    assignments = set()
    for assignment in itertools.product([True, False], repeat=len(cnf)):
        if all(assignment[i - 1] == (l > 0) == l in clause for clause in cnf for l in clause):
            assignments.add(tuple(assignment))
    
    group_actions = []
    for i in range(len(assignments)):
        for j in range(i + 1, len(assignments)):
            if all(not (assignments[i][k] == assignments[j][k]) for k in range(len(assignments))):
                group_actions.append((i, j))
    
    return len(group_actions)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            m = random.randint(n, 2 * n)
            cnf = generate_cnf(m, n)
            proof_depth = resolution(cnf)
            group_order = geometric_group_action(cnf)
            results.append((proof_depth, group_order))
    
    if not results:
        return {
            "metric_name": "resolution_proof_depth",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_proof_depth = sum(proof_depth for proof_depth, _ in results) / len(results)
    std_proof_depth = math.sqrt(sum((proof_depth - mean_proof_depth) ** 2 for proof_depth, _ in results) / len(results))
    upper_bound = (m * n) ** 2 * math.log(n)
    
    if any(proof_depth > upper_bound + 0.3 * upper_bound for _, proof_depth in results):
        return {
            "metric_name": "resolution_proof_depth",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(m for _, _ in results),
            "conjecture_holds": False,
            "counterexample": f"proof depth exceeds upper bound by more than 30%"
        }
    
    if all(abs(proof_depth - upper_bound) <= 0.3 * upper_bound for proof_depth, _ in results):
        return {
            "metric_name": "resolution_proof_depth",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(m for _, _ in results),
            "conjecture_holds": True,
            "counterexample": ""
        }
    
    return {
        "metric_name": "resolution_proof_depth",
        "metric_value": None,
        "instances_tested": len(results),
        "n_max": max(m for _, _ in results),
        "conjecture_holds": False,
        "counterexample": f"no significant linear relationship found"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    support_count = sum(1 for r in results if r["conjecture_holds"])
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    
    if support_count >= 0.8 * len(seeds):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_count/len(seeds)}")
    elif any(r["conjecture_holds"] is False for r in results):
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"no significant linear relationship found\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")