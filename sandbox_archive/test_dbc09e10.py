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

def lex_dpll(F):
    stack = []
    assignment = {}
    def unit_propagation():
        while True:
            found_unit_clause = False
            for clause in F:
                if len(clause) == 1 and clause[0] not in assignment:
                    assignment[clause[0]] = True
                    found_unit_clause = True
                    stack.append((clause[0], True))
                elif -clause[0] in assignment and assignment[-clause[0]]:
                    return False
            if not found_unit_clause:
                break
    def backtracking():
        while stack:
            var, val = stack.pop()
            assignment[var] = not val
            for clause in F:
                if var in clause:
                    clause.remove(var)
                if -var in clause and len(clause) == 1:
                    return False
            unit_propagation()
    unit_propagation()
    backtracking()
    return assignment

def width_2_rup_closure(F, max_rounds=200):
    n = len(F[0])
    closure = F[:]
    for _ in range(max_rounds):
        new_clauses = []
        for clause in closure:
            if len(clause) == 2:
                new_clause = [x for x in closure if x != clause and -x not in clause]
                if new_clause:
                    new_clauses.append(new_clause)
        if not new_clauses:
            break
        closure.extend(new_clauses)
    return closure

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [6, 8, 10, 12]
    alpha_values = [4.5, 5.0, 6.0]
    violation_count = 0
    total_instances = 0

    for n in n_values:
        for alpha in alpha_values:
            m = int(alpha * n)
            F = []
            while len(F) < m:
                clause = [random.randint(1, n), random.randint(1, n), random.randint(1, n)]
                if clause not in F and -clause not in F:
                    F.append(clause)
            assignment = lex_dpll(F)
            if assignment is None:
                continue
            total_instances += 1
            r_2_F = width_2_rup_closure(F)
            L_F = len(lex_dpll(r_2_F))
            if r_2_F and math.log2(L_F) > 2 * len(r_2_F) + 2 * math.log2(n + 1):
                violation_count += 1
            elif not r_2_F and math.log2(L_F) < n / 4:
                violation_count += 1

    conjecture_holds = violation_count == 0
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "violation_count",
        "metric_value": violation_count,
        "instances_tested": total_instances,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
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
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print("RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed=<s>")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")