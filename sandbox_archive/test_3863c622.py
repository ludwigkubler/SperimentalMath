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

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def truth_table_to_cnf(truth_table):
    n = len(truth_table)
    variables = list(range(n))
    clauses = []
    for i in range(2**n):
        row = truth_table[i]
        if sum(row) == 0:
            continue
        clause = []
        for j in range(n):
            if row[j] == 1:
                clause.append(variables[j])
            else:
                clause.append(-variables[j])
        clauses.append(clause)
    return clauses

def dpll(cnf, assignment={}):
    if not cnf:
        return True
    unit_clause = next((c for c in cnf if len(c) == 1), None)
    if unit_clause:
        var = unit_clause[0]
        new_assignment = assignment.copy()
        new_assignment[var] = var > 0
        return dpll([cl for cl in cnf if var not in cl and -var not in cl], new_assignment)
    pure_literal = next((v for v in variables if all(v in c or -v in c for c in cnf)), None)
    if pure_literal is not None:
        new_assignment = assignment.copy()
        new_assignment[pure_literal] = True
        return dpll([cl for cl in cnf if pure_literal not in cl and -pure_literal not in cl], new_assignment)
    var = random.choice(variables)
    if dpll(cnf, {**assignment, var: True}):
        return True
    if dpll(cnf, {**assignment, var: False}):
        return True
    return False

def resolution_proof_width(truth_table):
    cnf = truth_table_to_cnf(truth_table)
    assignment = {}
    stack = []
    while True:
        unit_clause = next((c for c in cnf if len(c) == 1), None)
        if unit_clause:
            var = unit_clause[0]
            assignment[var] = var > 0
            cnf = [cl for cl in cnf if var not in cl and -var not in cl]
        else:
            pure_literal = next((v for v in variables if all(v in c or -v in c for c in cnf)), None)
            if pure_literal is not None:
                assignment[pure_literal] = True
                cnf = [cl for cl in cnf if pure_literal not in cl and -pure_literal not in cl]
            else:
                var = random.choice(variables)
                stack.append((var, True))
                if dpll(cnf, {**assignment, var: True}):
                    assignment[var] = True
                    cnf = [cl for cl in cnf if var not in cl and -var not in cl]
                else:
                    assignment[var] = False
                    cnf = [cl for cl in cnf if var not in cl and -var not in cl]
        if not cnf:
            return len(stack)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in range(5, 41):
        truth_table = generate_boolean_function(n)
        width = resolution_proof_width(truth_table)
        results.append(width)
    M_f = sum(results) / len(results)
    return {
        "metric_name": "resolution_proof_width",
        "metric_value": M_f,
        "instances_tested": 36,
        "n_max": 40,
        "conjecture_holds": M_f <= 2 * n and M_f >= n / 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    mean = sum(results) / len(results)
    std_dev = (sum((x - mean) ** 2 for x in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r <= 2 * n and r >= n / 2) / len(results)
    if all(r <= 2 * n and r >= n / 2 for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not (r <= 2 * n and r >= n / 2))
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={seeds[first_failing_seed]}")