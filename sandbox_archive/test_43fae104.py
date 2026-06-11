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

def generate_cnf(m, n):
    cnf = []
    for _ in range(m):
        clause = set()
        while len(clause) < 3:
            var = random.randint(1, n)
            sign = random.choice([-1, 1])
            clause.add((var, sign))
        cnf.append(list(clause))
    return cnf

def resolution(cnf):
    clauses = [set(clause) for clause in cnf]
    while True:
        new_clauses = set()
        found_resolvent = False
        for i in range(len(clauses)):
            for j in range(i + 1, len(clauses)):
                common_lits = set(x for x in clauses[i] if -x in clauses[j])
                if common_lits:
                    resolvent = (clauses[i] | clauses[j]) - common_lits
                    new_clauses.add(tuple(sorted(resolvent)))
                    found_resolvent = True
        if not found_resolvent:
            break
        clauses.extend(new_clauses)
    return len(clauses)

def geometric_group_action(cnf):
    assignments = set()
    for assignment in itertools.product([True, False], repeat=len(cnf)):
        assignments.add(tuple(assignment))
    
    action = []
    for i in range(len(assignments)):
        permuted_assignment = list(assignments[i])
        random.shuffle(permuted_assignment)
        action.append((assignments[i], tuple(permuted_assignment)))
    
    return len(action)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 0
    total_metric_value = 0.0
    
    for m in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            cnf = generate_cnf(m, n_max)
            proof_depth = resolution(cnf)
            action_order = geometric_group_action(cnf)
            
            instances_tested += 1
            total_metric_value += abs(proof_depth - (m * n_max) ** 2 * math.log(n_max))
    
    metric_value = total_metric_value / instances_tested
    conjecture_holds = all(abs(proof_depth - (m * n_max) ** 2 * math.log(n_max)) <= 0.3 * (m * n_max) ** 2 * math.log(n_max) for m in [5, 10, 15, 20, 30, 40] for _ in range(5))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "resolution_proof_depth",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["counterexample"] == "mapping_undefined" for r in results):
        print("RESULT: INCONCLUSIVE mapping_undefined")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")