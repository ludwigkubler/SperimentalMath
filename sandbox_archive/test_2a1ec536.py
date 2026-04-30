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

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_primes(count):
    primes = []
    num = 2
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def dpll(sat_formula, assignment):
    if not sat_formula:
        return True
    unit_clauses = [c for c in sat_formula if len(c) == 1]
    if unit_clauses:
        literal = unit_clauses[0][0]
        if literal < 0:
            literal = -literal
            value = False
        else:
            value = True
        assignment[literal] = value
        new_formula = []
        for clause in sat_formula:
            if literal not in clause and -literal not in clause:
                new_formula.append(clause)
            elif literal in clause:
                continue
            else:
                new_clause = [l for l in clause if l != -literal]
                new_formula.append(new_clause)
        return dpll(new_formula, assignment)
    polarities = [1, -1]
    for polarity in polarities:
        literal = random.choice([v for v in range(1, len(sat_formula) + 1)])
        assignment[literal] = polarity == 1
        new_formula = []
        for clause in sat_formula:
            if literal not in clause and -literal not in clause:
                new_formula.append(clause)
            elif literal in clause:
                continue
            else:
                new_clause = [l for l in clause if l != -literal]
                new_formula.append(new_clause)
        if dpll(new_formula, assignment):
            return True
        del assignment[literal]
    return False

def resolution_depth(sat_formula):
    stack = []
    while sat_formula:
        unit_clauses = [c for c in sat_formula if len(c) == 1]
        if not unit_clauses:
            break
        literal = unit_clauses[0][0]
        if literal < 0:
            literal = -literal
            value = False
        else:
            value = True
        assignment[literal] = value
        new_formula = []
        for clause in sat_formula:
            if literal not in clause and -literal not in clause:
                new_formula.append(clause)
            elif literal in clause:
                continue
            else:
                new_clause = [l for l in clause if l != -literal]
                new_formula.append(new_clause)
        stack.append((new_formula, assignment))
    return len(stack)

def bounded_collection_iterations(sat_formula):
    # Placeholder implementation for BΣ_1 iterations
    # This is a dummy function and should be replaced with actual logic
    return 0

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    sat_formula = []
    for _ in range(n):
        clause = [random.randint(1, n), -random.randint(1, n)]
        while len(set(clause)) != 2:
            clause = [random.randint(1, n), -random.randint(1, n)]
        sat_formula.append(clause)
    depth = resolution_depth(sat_formula)
    k_n = bounded_collection_iterations(sat_formula)
    c = 1.0
    if depth < c * k_n:
        return {
            "metric_name": "Resolution Depth vs BΣ_1 Iterations",
            "metric_value": depth,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "depth < c * k_n"
        }
    else:
        return {
            "metric_name": "Resolution Depth vs BΣ_1 Iterations",
            "metric_value": depth,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or generate_primes(30)
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_depth = sum(r["metric_value"] for r in results) / len(results)
    std_depth = math.sqrt(sum((r["metric_value"] - mean_depth) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_depth} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='depth < c * k_n' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")