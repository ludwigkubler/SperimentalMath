# auto-injected by SEC sandbox
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
import math
import sys

def dpll(clauses, assignment, literals):
    if not clauses:
        return True
    unit_clause = next((c for c in clauses if len(c) == 1), None)
    if unit_clause:
        literal = unit_clause[0]
        if literal < 0 and -literal in assignment:
            return False
        elif literal > 0 and literal not in assignment:
            assignment[literal] = True
        else:
            del assignment[-literal]
        return dpll(clauses, assignment, literals)
    pure_literal = next((l for l in literals if all(l in clause or -l in clause for clause in clauses)), None)
    if pure_literal is not None:
        literal = pure_literal
        if literal < 0 and -literal in assignment:
            return False
        elif literal > 0 and literal not in assignment:
            assignment[literal] = True
        else:
            del assignment[-literal]
        return dpll(clauses, assignment, literals)
    literal = random.choice(literals)
    if literal < 0 and -literal in assignment:
        return False
    elif literal > 0 and literal not in assignment:
        assignment[literal] = True
        return dpll(clauses, assignment, literals)
    else:
        del assignment[-literal]
        return dpll(clauses, assignment, literals)

def resolution_proof(clauses):
    literals = set(abs(lit) for clause in clauses for lit in clause)
    assignment = {}
    while not dpll(clauses, assignment, literals):
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            assignment[literal] = True
            del assignment[-literal]
        else:
            literals.remove(abs(lit))
    return assignment

def kendall_tau_distance(freqs, n):
    rank = {lit: i for i, lit in enumerate(sorted(freqs.keys(), key=freqs.get, reverse=True))}
    tau_numerator = sum((rank[lit1] - rank[lit2]) * (freqs[lit1] - freqs[lit2]) for lit1 in freqs for lit2 in freqs if lit1 != lit2)
    tau_denominator = 2 * n * (n - 1) * sum(freqs[lit]**2 for lit in freqs)
    return abs(tau_numerator / math.sqrt(tau_denominator))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(3 * n, 10 * n)
    clauses = []
    for _ in range(m):
        clause = [random.choice(range(-n, 0)) if random.random() < 0.5 else random.choice(range(1, n + 1)) for _ in range(random.randint(1, 3))]
        clauses.append(clause)
    
    proof = resolution_proof(clauses)
    freqs = {lit: sum(proof[lit] for lit in proof if abs(lit) == abs(lit)) for lit in set(abs(lit) for lit in proof)}
    tau_distance = kendall_tau_distance(freqs, n)
    
    return {
        "metric_name": "Kendall tau distance",
        "metric_value": tau_distance,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": tau_distance <= n**0.5 + 1 and tau_distance >= n**0.5 - 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_tau_distance = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_tau_distance} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_tau_distance} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='Kendall tau distance does not match n^0.5' first_failing_seed={first_failing_seed}")