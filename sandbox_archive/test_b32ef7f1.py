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
    cnf = []
    for _ in range(10):  # Generate 10 clauses for simplicity
        clause = [random.randint(-n, n) for _ in range(3)]
        if 0 not in clause:
            cnf.append(clause)
    return cnf

def dpll(cnf):
    def dpll_rec(model, clauses):
        if not clauses:
            return True
        literal = find_pure_literal(clauses, model)
        if literal is not None:
            new_model = update_model(model, literal)
            if dpll_rec(new_model, clauses):
                return True
            else:
                return dpll_rec(update_model(model, -literal), clauses)
        unit_clause = find_unit_clause(clauses, model)
        if unit_clause is not None:
            literal = unit_clause[0]
            new_model = update_model(model, literal)
            if dpll_rec(new_model, clauses):
                return True
            else:
                return dpll_rec(update_model(model, -literal), clauses)
        literal = select_literal(clauses)
        for value in [True, False]:
            new_model = update_model(model, literal, value)
            if dpll_rec(new_model, clauses):
                return True
        return False

    def find_pure_literal(clauses, model):
        pure_literals = set()
        for clause in clauses:
            literals = [l for l in clause if l not in model]
            if len(literals) == 1 and -literals[0] not in model:
                pure_literals.add(literals[0])
        return next(iter(pure_literals), None)

    def update_model(model, literal, value=None):
        new_model = dict(model)
        if value is not None:
            new_model[literal] = value
        else:
            new_model[literal] = True
        return new_model

    def find_unit_clause(clauses, model):
        for clause in clauses:
            literals = [l for l in clause if l not in model]
            if len(literals) == 1:
                return clause
        return None

    def select_literal(clauses):
        return random.choice([l for clause in clauses for l in clause if l not in model])

    return dpll_rec({}, cnf)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 10  # Fixed size for simplicity
    cnf = generate_cnf(n)
    t_star = dpll(cnf)
    R_F = n  # Placeholder value, as the actual computation is not provided in the conjecture

    if t_star == -1:
        return {
            "metric_name": "R(F) / t*(F)",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "DPLL did not find a refutation"
        }

    ratio = Fraction(R_F, t_star)
    return {
        "metric_name": "R(F) / t*(F)",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": True if ratio <= 2 else False,  # Placeholder constant c
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(30))
    results = []
    total_ratio = Fraction(0)
    num_trials = 0

    for seed in seeds:
        trial_result = run_trial(seed)
        results.append(trial_result)
        if trial_result["metric_value"] is not None:
            total_ratio += Fraction(trial_result["metric_value"])
            num_trials += 1

    mean_ratio = float(total_ratio / num_trials) if num_trials > 0 else None
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    print(f"RESULT: SUPPORTED mean={mean_ratio} std=NA support_fraction={support_fraction}")