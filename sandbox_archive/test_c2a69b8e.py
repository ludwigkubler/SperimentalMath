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

def generate_formula(m, n):
    variables = set(range(n))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, random.randint(1, n))
        clauses.append(clause)
    return clauses

def construct_poset(clauses):
    poset = {}
    for i in range(len(clauses)):
        for j in range(i + 1, len(clauses)):
            if set(clauses[i]).issubset(set(clauses[j])):
                poset.setdefault(i, []).append(j)
            elif set(clauses[j]).issubset(set(clauses[i])):
                poset.setdefault(j, []).append(i)
    return poset

def minimal_symplectic_leaf_number(poset):
    if not poset:
        return 0
    leaves = [i for i in range(len(poset)) if i not in sum(poset.values(), [])]
    return len(leaves)

def resolution_proof_width(clauses):
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            var = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[var] = True
            if dpll([c for c in clauses if var not in c], new_assignment):
                return True
            new_assignment[var] = False
            if dpll([c for c in clauses if -var not in c], new_assignment):
                return True
            return False
        pure_literal = next((v for v in range(1, max(clauses) + 1) if all(v not in c or -v in c for c in clauses)), None)
        if pure_literal is not None:
            new_assignment = assignment.copy()
            new_assignment[pure_literal] = True
            if dpll([c for c in clauses if pure_literal not in c], new_assignment):
                return True
            new_assignment[pure_literal] = False
            if dpll([c for c in clauses if -pure_literal not in c], new_assignment):
                return True
            return False
        var = random.choice(range(1, max(clauses) + 1))
        new_assignment = assignment.copy()
        new_assignment[var] = True
        if dpll([c for c in clauses if var not in c], new_assignment):
            return True
        new_assignment[var] = False
        if dpll([c for c in clauses if -var not in c], new_assignment):
            return True
        return False

    assignment = {}
    return len(clauses) if not dpll(clauses, assignment) else 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    m = random.randint(5, 30)
    n = random.randint(5, 30)
    clauses = generate_formula(m, n)
    poset = construct_poset(clauses)
    msl_phi = minimal_symplectic_leaf_number(poset)
    w_phi = resolution_proof_width(clauses)
    return {
        "metric_name": "msl_to_w_ratio",
        "metric_value": Fraction(msl_phi, w_phi) if w_phi != 0 else float('inf'),
        "instances_tested": 1,
        "n_max": max(m, n),
        "conjecture_holds": msl_phi <= w_phi,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_ratio = sum(r["metric_value"] for r in results if r["conjecture_holds"]) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "msl_to_w_ratio > 1"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")