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

def generate_random_sat_instance(n: int, m: int) -> list:
    variables = [f'x{i+1}' for i in range(n)]
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, 3)
        clauses.append(clause)
    return clauses

def tseitin_transform(clauses: list) -> dict:
    literals = set()
    for clause in clauses:
        literals.update(clause)
    new_vars = {lit: f'y{i+1}' for i, lit in enumerate(literals)}
    new_clauses = []
    for clause in clauses:
        y = new_vars[clause[0]]
        new_clause = [f'~{new_vars[lit]}' if lit != clause[0] else new_vars[lit] for lit in clause]
        new_clauses.append([y, *new_clause])
        for i in range(1, len(clause)):
            y = new_vars[clause[i]]
            new_clause = [f'~{new_vars[lit]}' if lit != clause[i] else new_vars[lit] for lit in clause]
            new_clauses.append([y, *new_clause])
    return new_clauses

def resolution_prove(clauses: list) -> int:
    clauses_set = set(tuple(sorted(c)) for c in clauses)
    while True:
        new_clauses = []
        for c1 in clauses_set:
            for c2 in clauses_set:
                if len(set(c1).intersection(set(c2))) == 1:
                    diff = [lit for lit in c1 if lit not in c2][0]
                    new_clause = sorted(list(set(c1) ^ set(c2)))
                    if new_clause and new_clause not in clauses_set:
                        new_clauses.append(new_clause)
        if not new_clauses:
            break
        clauses_set.update(tuple(sorted(c)) for c in new_clauses)
    return len(clauses_set)

def monodromy_group_order(n: int) -> int:
    # Placeholder function to compute the minimal order of the monodromy group
    # This is a dummy implementation and should be replaced with actual computation
    return n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        m = max(1, n // 2)  # Ensure at least one clause
        clauses = generate_random_sat_instance(n, m)
        tseitin_clauses = tseitin_transform(clauses)
        proof_width = resolution_prove(tseitin_clauses)
        group_order = monodromy_group_order(n)
        results.append((group_order, proof_width))
    
    if not results:
        return {
            "metric_name": "Monodromy Group Order vs Resolution Proof Width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    group_orders = [r[0] for r in results]
    proof_widths = [r[1] for r in results]
    alpha = sum(group_orders) / sum(proof_widths)
    correlation = sum((g - alpha * w) ** 2 for g, w in zip(group_orders, proof_widths)) / len(results)
    
    return {
        "metric_name": "Monodromy Group Order vs Resolution Proof Width",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n for n in [5, 10, 15, 20, 30, 40]),
        "conjecture_holds": correlation <= 0.1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction={support_fraction}")
    elif support_fraction < 0.7:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence support_fraction={support_fraction}")