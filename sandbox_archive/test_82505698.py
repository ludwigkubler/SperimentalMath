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
from fractions import Fraction
import math
import itertools

def generate_satisfying_assignments(cnf, k):
    n = len(cnf)
    assignments = []
    for _ in range(k):
        assignment = [random.choice([-1, 1]) for _ in range(n)]
        if all(any(lit == assignment[abs(lit) - 1] * sign for lit, sign in clause) for clause in cnf):
            assignments.append(assignment)
    return assignments

def generate_cnf(n, m):
    cnf = []
    literals = list(range(-n, 0)) + list(range(1, n + 1))
    for _ in range(m):
        clause = random.sample(literals, random.randint(2, n))
        cnf.append(clause)
    return cnf

def compute_quotient_group_order(cnf, assignments):
    n = len(cnf)
    S_n = list(itertools.permutations(range(n)))
    kernel = set()
    
    for perm in S_n:
        if all(any(perm[abs(lit) - 1] * sign == assignment[abs(lit) - 1] * sign for lit, sign in clause) for clause in cnf):
            kernel.add(tuple(perm))
    
    quotient_group_order = len(S_n) // len(kernel)
    return quotient_group_order

def compute_frege_proof_depth(cnf):
    # Simplified DPLL solver to estimate proof depth
    def dpll(clauses, assignment, model):
        if not clauses:
            return 0
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment[:]
            new_model = model.copy()
            if literal > 0:
                new_assignment[literal - 1] = 1
                new_model.add(literal)
            else:
                new_assignment[-literal - 1] = -1
                new_model.remove(-literal)
            return 1 + dpll(clauses, new_assignment, new_model)
        pure_literal = next((l for l in range(1, n + 1) if (l not in model and -l not in model)), None)
        if pure_literal:
            new_assignment = assignment[:]
            new_model = model.copy()
            if pure_literal > 0:
                new_assignment[pure_literal - 1] = 1
                new_model.add(pure_literal)
            else:
                new_assignment[-pure_literal - 1] = -1
                new_model.remove(-pure_literal)
            return 1 + dpll(clauses, new_assignment, new_model)
        return float('inf')
    
    proof_depth = min(dpll(cnf, [0] * n, set()) for _ in range(10))
    return proof_depth

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 30
    m = 2 * n
    cnf = generate_cnf(n, m)
    assignments = generate_satisfying_assignments(cnf, 50)
    
    if not assignments:
        return {
            "metric_name": "quotient_group_order",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "no_satisfying_assignments"
        }
    
    quotient_group_order = compute_quotient_group_order(cnf, assignments)
    proof_depth = compute_frege_proof_depth(cnf)
    
    return {
        "metric_name": "quotient_group_order",
        "metric_value": quotient_group_order,
        "instances_tested": len(assignments),
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_count = sum(1 for r in results if r["conjecture_holds"])
    support_fraction = support_count / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='not_enough_support' first_failing_seed={first_failing_seed}")