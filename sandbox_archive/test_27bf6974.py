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

def generate_cnf(n):
    clauses = []
    for _ in range(2 * n):
        clause = [random.choice([f"v{i+1}", f"~v{i+1}"]) for _ in range(random.randint(1, 3))]
        clauses.append(clause)
    return clauses

def construct_formal_context(cnf):
    universe = set()
    relation = {}
    for clause in cnf:
        for literal in clause:
            universe.add(literal[2:] if literal.startswith('~') else literal)
            if literal not in relation:
                relation[literal] = set()
            for other_literal in clause:
                if literal != other_literal and (other_literal[2:] if other_literal.startswith('~') else other_literal) not in relation[literal]:
                    relation[literal].add(other_literal[2:] if other_literal.startswith('~') else other_literal)
    return universe, relation

def minimal_order(universe, relation):
    max_subcontext_size = 0
    for literal in universe:
        subcontext = {literal}
        queue = list(subcontext)
        while queue:
            current = queue.pop()
            for neighbor in relation.get(current, set()):
                if neighbor not in subcontext:
                    subcontext.add(neighbor)
                    queue.append(neighbor)
        max_subcontext_size = max(max_subcontext_size, len(subcontext))
    return max_subcontext_size

def dpll_proof_width(cnf):
    def dpll(clauses, assignment):
        if not clauses:
            return 0
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if all(l.startswith('~') and not new_assignment[l[2:]] or not l.startswith('~') and new_assignment[l] for l in clauses):
                return 1 + dpll([c for c in clauses if literal not in c], new_assignment)
            else:
                return 1 + dpll([c for c in clauses if literal not in c], {**new_assignment, literal: False})
        pure_literal = next((l for l in universe if all(l.startswith('~') and not assignment[l[2:]] or not l.startswith('~') and assignment[l] for c in clauses for l in c) and not any(l.startswith('~') and assignment[l[2:]] or not l.startswith('~') and not assignment[l] for c in clauses for l in c)), None)
        if pure_literal:
            new_assignment = assignment.copy()
            new_assignment[pure_literal] = True
            return 1 + dpll([c for c in clauses if pure_literal not in c], new_assignment)
        else:
            literal = random.choice(list(universe))
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            return 1 + dpll([c for c in clauses if literal not in c], new_assignment)

    universe = set()
    for clause in cnf:
        for literal in clause:
            universe.add(literal[2:] if literal.startswith('~') else literal)
    assignment = {v: False for v in universe}
    return dpll(cnf, assignment)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    cnf = generate_cnf(n)
    universe, relation = construct_formal_context(cnf)
    minimal_order_value = minimal_order(universe, relation)
    proof_width_value = dpll_proof_width(cnf)
    return {
        "metric_name": "Minimal Order",
        "metric_value": minimal_order_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": minimal_order_value == proof_width_value,
        "counterexample": "" if minimal_order_value == proof_width_value else f"Order: {minimal_order_value}, Width: {proof_width_value}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Order does not match Width\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")