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

def dpll(cnf, assignment):
    def propagate():
        changed = False
        for clause in cnf:
            if len(clause) == 1:
                literal = clause[0]
                var = abs(literal)
                if literal > 0 and var not in assignment:
                    assignment[var] = True
                    changed = True
                elif literal < 0 and var not in assignment:
                    assignment[var] = False
                    changed = True
        return changed

    def unit_propagation():
        while propagate():
            pass

    def pure_literal_sweep(literal):
        for clause in cnf:
            if literal in clause:
                clause.remove(literal)
                if len(clause) == 0:
                    return False
            elif -literal in clause:
                clause.remove(-literal)
        return True

    while True:
        unit_propagation()
        changed = False
        for var in range(1, max(assignment.keys()) + 1):
            if var not in assignment:
                if pure_literal_sweep(var) and pure_literal_sweep(-var):
                    continue
                else:
                    assignment[var] = True
                    changed = True
        if not changed:
            return assignment

def generate_3cnf(n, m):
    cnf = set()
    while len(cnf) < m:
        clause = {random.randint(1, n), random.randint(-n, -1)}
        if len(clause) == 2 and all(abs(lit) not in clause for lit in cnf):
            cnf.add(tuple(sorted(clause)))
    return cnf

def upc(cnf):
    assignment = {}
    while True:
        unit_propagation(cnf, assignment)
        changed = False
        for var in range(1, 13):
            if var not in assignment:
                assignment[var] = False
                unit_propagation(cnf, assignment)
                if is_conflicting(cnf, assignment):
                    assignment[var] = True
                    changed = True
                else:
                    assignment.pop(var)
        if not changed:
            return "⊥"

def is_conflicting(cnf, assignment):
    for clause in cnf:
        if all(lit not in assignment or assignment[lit] == (lit > 0) for lit in clause):
            return True
    return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 12
    m = math.floor(4.27 * n)
    cnf = generate_3cnf(n, m)
    if dpll(cnf, {}) is None:
        return {
            "metric_name": "UPC",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "unsatisfiable"
        }
    upc_result = upc(cnf)
    return {
        "metric_name": "UPC",
        "metric_value": 1 if upc_result == "⊥" else 0,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    p_hat = sum(r["metric_value"] for r in results) / len(results)
    se = math.sqrt(p_hat * (1 - p_hat) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if p_hat <= 0.20 and (0.20 - p_hat) >= 3 * se:
        print(f"RESULT: SUPPORTED mean={p_hat} std={se} support_fraction={support_fraction}")
    elif p_hat > 0.20 and (p_hat - 0.20) >= 3 * se:
        print(f"RESULT: FALSIFIED counterexample=\"upc_success\" first_failing_seed={seeds[results.index(next(r for r in results if not r['conjecture_holds']))]}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")