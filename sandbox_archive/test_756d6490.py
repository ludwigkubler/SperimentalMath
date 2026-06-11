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

def generate_satisfying_assignments(cnf, k):
    n = len(cnf)
    assignments = []
    for _ in range(k):
        assignment = [random.choice([-1, 1]) for _ in range(n)]
        if all(any(lit == assignment[abs(lit) - 1] * sign for lit, sign in clause) for clause in cnf):
            assignments.append(assignment)
    return assignments

def compute_quotient_group_order(cnf, assignments):
    n = len(cnf)
    S_n = list(itertools.permutations(range(n)))
    kernel = set()
    for perm in S_n:
        if all((perm[i] + 1) % n == (i + 1) % n for i in range(n)):
            kernel.add(perm)
    quotient_group_order = len(S_n) // len(kernel)
    return quotient_group_order

def compute_frege_proof_depth(cnf):
    # Simplified DPLL solver to estimate proof depth
    def dpll(clauses, assignment):
        if not clauses:
            return 1
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment[:]
            new_assignment[abs(literal) - 1] *= literal // abs(literal)
            return dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment)
        pure_literal = next((l for l in range(1, n + 1) if sum(c.count(l) for c in clauses) == 0 or sum(c.count(-l) for c in clauses) == 0), None)
        if pure_literal:
            return dpll(clauses, assignment + [pure_literal])
        return max(dpll([c for c in clauses if literal not in c and -literal not in c], assignment + [literal]) for literal in range(1, n + 1))

    proof_depth = dpll(cnf, [])
    return proof_depth

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = [[random.choice([-i, i]) for _ in range(random.randint(2, n))] for _ in range(n)]
    assignments = generate_satisfying_assignments(cnf, 30)
    quotient_group_order = compute_quotient_group_order(cnf, assignments)
    frege_proof_depth = compute_frege_proof_depth(cnf)
    
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
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_order = sum(r["metric_value"] for r in results) / len(results)
    std_order = math.sqrt(sum((r["metric_value"] - mean_order) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_order} std={std_order} support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_order} std={std_order} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")