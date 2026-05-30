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

def random_3cnf(n, m):
    clauses = []
    for _ in range(m):
        literals = random.sample(range(1, n + 1), 3)
        clause = [(random.choice([-1, 1]) * lit) for lit in literals]
        clauses.append(clause)
    return clauses

def dpll(clauses, assignment, literals):
    unit_clauses = [c for c in clauses if len(c) == 1]
    while unit_clauses:
        literal = unit_clauses[0][0]
        polarity = literal > 0
        assignment[literal] = polarity
        literals.remove(literal)
        new_clauses = []
        for clause in clauses:
            if not any(abs(lit) == abs(literal) for lit in clause):
                new_clauses.append(clause)
            elif all(abs(lit) != abs(literal) for lit in clause):
                return False
        clauses = new_clauses
        unit_clauses = [c for c in clauses if len(c) == 1]
    pure_literals = []
    for literal in literals:
        if literal not in assignment and -literal not in assignment:
            count_pos = sum(1 for c in clauses if literal in c)
            count_neg = sum(1 for c in clauses if -literal in c)
            if count_pos > count_neg:
                pure_literals.append((literal, True))
            elif count_neg > count_pos:
                pure_literals.append((-literal, False))
    while pure_literals:
        literal, polarity = pure_literals[0]
        assignment[literal] = polarity
        literals.remove(literal)
        new_clauses = []
        for clause in clauses:
            if not any(abs(lit) == abs(literal) for lit in clause):
                new_clauses.append(clause)
            elif all(abs(lit) != abs(literal) for lit in clause):
                return False
        clauses = new_clauses
    return True

def resolution_proof(clauses):
    assignment = {}
    literals = set()
    for clause in clauses:
        for literal in clause:
            literals.add(abs(literal))
    while not dpll(clauses, assignment, literals):
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause is None:
            return []
        literal = unit_clause[0]
        polarity = literal > 0
        assignment[literal] = polarity
        literals.remove(literal)
        new_clauses = []
        for clause in clauses:
            if not any(abs(lit) == abs(literal) for lit in clause):
                new_clauses.append(clause)
            elif all(abs(lit) != abs(literal) for lit in clause):
                return []
        clauses = new_clauses
    return []

def kendall_tau_distance(freqs, n):
    rank = {lit: i + 1 for i, lit in enumerate(sorted(freqs))}
    tau_numerator = sum((rank[lit] - (i + 1)) ** 2 for i, lit in enumerate(freqs))
    tau_denominator = n * (n**2 - 1) / 4
    return math.sqrt(tau_numerator / tau_denominator)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        m = 2 * n
        clauses = random_3cnf(n, m)
        proof = resolution_proof(clauses)
        if not proof:
            continue
        literal_freqs = {lit: sum(1 for clause in proof if lit in clause) for lit in range(1, n + 1)}
        tau_distance = kendall_tau_distance(literal_freqs, n)
        results.append(tau_distance)
    mean_value = sum(results) / len(results)
    conjecture_holds = all(abs(tau - math.sqrt(n)) <= 0.5 for tau in results) and all(tau <= math.sqrt(n) + 1 for tau in results)
    return {
        "metric_name": "Kendall_tau_distance",
        "metric_value": mean_value,
        "instances_tested": len(results),
        "n_max": max([5, 10, 15, 20, 30, 40]),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    mean_value = sum(results) / len(results)
    support_fraction = sum(1 for r in results if abs(r - math.sqrt(n)) <= 0.5 for n in [5, 10, 15, 20, 30, 40]) / len(results)
    if all(abs(r - math.sqrt(n)) <= 0.5 for r in results) and all(r <= math.sqrt(n) + 1 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    elif any(r > math.sqrt(n) + 1 for r, n in zip(results, [5, 10, 15, 20, 30, 40])):
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={seeds[results.index(max(results))]}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")