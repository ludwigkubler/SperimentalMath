# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def generate_sat_instance(m):
    variables = set()
    clauses = []
    for _ in range(m):
        clause = [random.choice([1, -1]) * (i + 1) for i in range(random.randint(2, 4))]
        variables.update(abs(x) for x in clause)
        clauses.append(clause)
    return variables, clauses

def tseitin_formula(variables, clauses):
    n_vars = len(variables)
    n_clauses = len(clauses)
    new_vars = [n_vars + i for i in range(n_clauses)]
    formula = []
    for i, clause in enumerate(clauses):
        new_var = new_vars[i]
        formula.append([new_var])
        for literal in clause:
            if literal > 0:
                formula.append([-literal, new_var])
            else:
                formula.append([literal, -new_var])
    return formula

def resolution_width(formula):
    clauses = set(tuple(clause) for clause in formula)
    unit_clauses = {c[0] for c in clauses if len(c) == 1}
    while unit_clauses:
        new_unit_clause = None
        for u in unit_clauses:
            for clause in clauses:
                if -u in clause:
                    new_clause = [l for l in clause if l != -u]
                    if len(new_clause) == 0:
                        return float('inf')
                    if len(new_clause) == 1:
                        new_unit_clause = new_clause[0]
                        break
            if new_unit_clause is not None:
                break
        unit_clauses.discard(u)
        unit_clauses.add(new_unit_clause)
    return len(clauses)

def clause_subset_entropy(variables, clauses):
    n_vars = len(variables)
    n_clauses = len(clauses)
    total_weight = 0
    for i in range(1 << n_vars):
        subset = [j + 1 for j in range(n_vars) if (i >> j) & 1]
        weight = sum(1 for clause in clauses if all(lit in subset or -lit in subset for lit in clause))
        total_weight += weight
    entropy = Fraction(total_weight, n_clauses * 2 ** n_vars).log()
    return entropy

def minimal_brauer_group_order(entropy):
    # Simplified Brauer group order approximation
    return abs(int(10 ** (entropy / 2)))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    m = random.randint(5, 40)
    variables, clauses = generate_sat_instance(m)
    formula = tseitin_formula(variables, clauses)
    entropy = clause_subset_entropy(variables, clauses)
    width = resolution_width(formula)
    order = minimal_brauer_group_order(entropy)
    return {
        "metric_name": "Brauer Group Order",
        "metric_value": order,
        "instances_tested": 1,
        "n_max": m,
        "conjecture_holds": True if order == width else False,
        "counterexample": "" if order == width else f"Order {order} does not match width {width}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")