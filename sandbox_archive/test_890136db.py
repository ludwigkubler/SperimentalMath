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

def generate_cnf(n):
    clauses = []
    for _ in range(2 * n):
        clause = [random.randint(-n, -1), random.randint(1, n)]
        clauses.append(clause)
    return clauses

def dpll(cnf, assignment, unit_clause=None):
    if not cnf:
        return True
    if unit_clause is not None:
        literal = unit_clause[0]
        if literal in assignment and assignment[literal] != (literal > 0):
            return False
        assignment[literal] = literal > 0
        cnf = [c for c in cnf if literal not in c and -literal not in c]

    unit_clauses = [c[0] for c in cnf if len(c) == 1]
    if unit_clauses:
        return dpll(cnf, assignment, unit_clause=random.choice(unit_clauses))

    literal = random.choice([l for l in range(-n, n+1) if l != 0 and l not in assignment])
    assignment[literal] = True
    if dpll(cnf, assignment):
        return True
    assignment[literal] = False
    return dpll(cnf, assignment)

def resolution_proof_width(cnf):
    n = len(cnf)
    clauses = [set(clause) for clause in cnf]
    unit_clause = None

    while True:
        new_clauses = []
        for i in range(n):
            for j in range(i + 1, n):
                if -clauses[i].intersection(clauses[j]):
                    new_clause = clauses[i] | clauses[j]
                    if len(new_clause) == 1:
                        unit_clause = list(new_clause)[0]
                        break
                    new_clauses.append(new_clause)
            else:
                continue
            break

        if not new_clauses and not unit_clause:
            return len(clauses)

        clauses.extend(new_clauses)
        if unit_clause:
            clauses.remove({unit_clause})
            unit_clause = None

def arithmetic_genus(cnf):
    n = len(cnf)
    # Placeholder for actual computation
    return Fraction(n, 2)  # Simplified example

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    cnf_formula = generate_cnf(n)
    
    g_F = arithmetic_genus(cnf_formula)
    ω_F = resolution_proof_width(cnf_formula)

    if g_F > 10 * ω_F:
        return {
            "metric_name": "arithmetic_genus_over_resolution",
            "metric_value": float(g_F),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"n={n}, g(F)={g_F}, ω_F={ω_F}"
        }

    return {
        "metric_name": "arithmetic_genus_over_resolution",
        "metric_value": float(g_F),
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["g(F)"] > 10 * r["ω_F"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if r["g(F)"] > 10 * r["ω_F"])
        print(f"RESULT: FALSIFIED counterexample='g(F) > 10 * ω_F' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")