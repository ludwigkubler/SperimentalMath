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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, m):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def rank_of_matrix(A):
    A = gaussian_elimination(A)
    rank = 0
    for row in A:
        if any(row):
            rank += 1
    return rank

def dpll(clauses, assignment, n):
    if not clauses:
        return True
    unit_clause = next((c for c in clauses if len(c) == 1), None)
    if unit_clause:
        literal = unit_clause[0]
        new_assignment = assignment.copy()
        new_assignment[literal] = literal > 0
        new_clauses = [c for c in clauses if not (literal in c or -literal in c)]
        return dpll(new_clauses, new_assignment, n)
    pure_literal = next((l for l in range(1, n+1) if all(l in c or -l in c for c in clauses)), None)
    if pure_literal is not None:
        new_assignment = assignment.copy()
        new_assignment[pure_literal] = True
        new_clauses = [c for c in clauses if not (pure_literal in c or -pure_literal in c)]
        return dpll(new_clauses, new_assignment, n)
    literal = random.choice([l for l in range(1, n+1) if l not in assignment])
    new_assignment_true = assignment.copy()
    new_assignment_true[literal] = True
    new_clauses_true = [c for c in clauses if not (literal in c or -literal in c)]
    if dpll(new_clauses_true, new_assignment_true, n):
        return True
    new_assignment_false = assignment.copy()
    new_assignment_false[literal] = False
    new_clauses_false = [c for c in clauses if not (-literal in c or literal in c)]
    return dpll(new_clauses_false, new_assignment_false, n)

def generate_random_sat_instance(n):
    m = random.randint(1, 2*n)
    clauses = []
    for _ in range(m):
        num_literals = random.randint(1, n)
        clause = set()
        while len(clause) < num_literals:
            literal = random.choice([l for l in range(-n, n+1) if l != 0])
            if -literal not in clause:
                clause.add(literal)
        clauses.append(list(clause))
    return clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested = 0
        total_rep_length = 0
        total_dpll_width = 0
        for _ in range(30):
            clauses = generate_random_sat_instance(n)
            assignment = {}
            rep_length = rank_of_matrix([[1 if l == i+1 else -1 if l == -(i+1) else 0 for l in range(-n, n+1)] for i in range(len(clauses))])
            dpll_width = dpll(clauses, assignment, n)
            total_rep_length += rep_length
            total_dpll_width += dpll_width
            instances_tested += 1
        if instances_tested < 30:
            return {"metric_name": "DPLLWidth vs DiophRepLength", "metric_value": None, "instances_tested": instances_tested, "n_max": n, "conjecture_holds": False, "counterexample": "insufficient_instances"}
        mean_rep_length = total_rep_length / instances_tested
        mean_dpll_width = total_dpll_width / instances_tested
        results.append((mean_rep_length, mean_dpll_width))
    correlation_coefficient = sum((x - mean_x) * (y - mean_y) for x, y in results) / (len(results) * math.sqrt(sum((x - mean_x)**2 for x, _ in results)) * math.sqrt(sum((y - mean_y)**2 for _, y in results)))
    p_value = 2 * (1 - 0.5 * (1 + correlation_coefficient))
    return {"metric_name": "DPLLWidth vs DiophRepLength", "metric_value": correlation_coefficient, "instances_tested": instances_tested, "n_max": max(n for n in [5, 10, 15, 20, 30, 40]), "conjecture_holds": correlation_coefficient > 0.8 and p_value < 0.05, "counterexample": ""}

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(1, 6)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    mean_value = sum(results) / len(results)
    std_value = math.sqrt(sum((x - mean_value)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r is not None and r > 0.8) / len(results)
    if all(r is not None and r > 0.8 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r is not None and r <= 0.8 for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(i for i, r in enumerate(results) if r is not None and r <= 0.8)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient<=0.8\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")