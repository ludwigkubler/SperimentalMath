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

def generate_kcnf(n, m):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = set()
        while len(clause) < 2:
            var = random.choice(variables)
            if -var not in clause:
                clause.add(var)
        clauses.append(tuple(sorted(clause)))
    return clauses

def dpll(formula, assignment, variables):
    if not formula:
        return True
    unit_clauses = [c for c in formula if len(c) == 1]
    if unit_clauses:
        var = unit_clauses[0][0]
        if -var in assignment:
            return False
        new_assignment = assignment.copy()
        new_assignment[var] = True
        return dpll([c for c in formula if var not in c and -var not in c], new_assignment, variables)
    pure_literals = {}
    for clause in formula:
        positive_vars = [v for v in clause if v > 0]
        negative_vars = [-v for v in clause if v < 0]
        for v in positive_vars:
            if v not in pure_literals:
                pure_literals[v] = True
            else:
                del pure_literals[v]
        for v in negative_vars:
            if -v not in pure_literals:
                pure_literals[-v] = False
            else:
                del pure_literals[-v]
    if pure_literals:
        var, value = next(iter(pure_literals.items()))
        new_assignment = assignment.copy()
        new_assignment[var] = value
        return dpll([c for c in formula if var not in c and -var not in c], new_assignment, variables)
    unassigned_var = next(v for v in variables if v not in assignment)
    return dpll(formula, {**assignment, unassigned_var: True}, variables) or dpll(formula, {**assignment, unassigned_var: False}, variables)

def generalized_hypergeometric_rank(clause):
    n = len(clause)
    rank = 1
    for i in range(1, n + 1):
        if all(x % i == 0 for x in clause):
            rank *= i
    return rank

def resolution_length(formula):
    assignment = {}
    variables = set(abs(v) for v in sum(formula, ()))
    return len(dpll(formula, assignment, variables))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n, n * 2)
    clauses = generate_kcnf(n, m)
    rank_sum = sum(generalized_hypergeometric_rank(c) for c in clauses)
    proof_length_sum = sum(resolution_length(clauses) for _ in range(30))
    metric_value = rank_sum / proof_length_sum if proof_length_sum > 0 else float('inf')
    conjecture_holds = metric_value < 2.0
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "rank_to_proof_length_ratio",
        "metric_value": metric_value,
        "instances_tested": m * 30,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results if r["conjecture_holds"]) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["conjecture_holds"]) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")