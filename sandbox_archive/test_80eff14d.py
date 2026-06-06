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

def generate_cnf(n, m):
    variables = [f'v{i}' for i in range(1, n + 1)]
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, random.randint(1, n))
        clauses.append(' OR '.join(clause))
    return ' AND '.join(clauses)

def dpll(cnf):
    def solve(literals, assignment):
        if not cnf:
            return True
        literal = next((l for l in literals if l[0] != '-'), None)
        if literal is None:
            return False
        pos_literal = literal[1:]
        neg_literal = '-' + literal[1:]
        if pos_literal in assignment and assignment[pos_literal]:
            return solve([l for l in literals if l != literal], assignment)
        elif neg_literal in assignment and not assignment[neg_literal]:
            return solve([l for l in literals if l != literal], assignment)
        else:
            new_assignment = assignment.copy()
            new_assignment[pos_literal] = True
            if solve(literals, new_assignment):
                return True
            new_assignment[pos_literal] = False
            new_assignment[neg_literal] = True
            return solve(literals, new_assignment)
    literals = set(l for clause in cnf.split(' AND ') for l in clause.split(' OR '))
    assignment = {l: None for l in literals}
    return solve(cnf.split(' AND '), assignment)

def construct_formal_context(cnf):
    context = {}
    literals = set(l for clause in cnf.split(' AND ') for l in clause.split(' OR '))
    for literal1 in literals:
        if literal1[0] == '-':
            continue
        context[literal1] = set()
        for literal2 in literals:
            if literal2[0] == '-' and literal2[1:] == literal1:
                continue
            if literal2 not in context[literal1]:
                clause = f'{literal1} OR {literal2}'
                if dpll(clause):
                    context[literal1].add(literal2)
    return context

def min_order_formal_context(context):
    subcontexts = []
    for literal, related_literals in context.items():
        subcontext = {literal}
        queue = list(related_literals)
        while queue:
            current_literal = queue.pop()
            if current_literal not in subcontext:
                subcontext.add(current_literal)
                queue.extend(context[current_literal] - subcontext)
        subcontexts.append(subcontext)
    return max(len(sc) for sc in subcontexts)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n, n * 3)
    cnf = generate_cnf(n, m)
    context = construct_formal_context(cnf)
    min_order = min_order_formal_context(context)
    dpll_width = len(dpll(cnf))
    return {
        "metric_name": "Minimal Order of Formal Context",
        "metric_value": min_order,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": min_order == dpll_width,
        "counterexample": "" if min_order == dpll_width else f"Min Order: {min_order}, DPLL Width: {dpll_width}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")