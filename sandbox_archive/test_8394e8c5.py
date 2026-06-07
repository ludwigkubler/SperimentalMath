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

def generate_random_cnf(n):
    cnf = []
    for _ in range(2 * n):  # Generate 2n clauses
        clause = [random.randint(-1, -2) for _ in range(random.randint(1, n))]
        if all(clause[j] != -clause[k] for k in range(len(clause)) for j in range(k)):
            cnf.append(clause)
    return cnf

def generate_random_prime(n):
    while True:
        p = random.randint(2**(n-1), 2**n - 1)
        if all(p % i != 0 for i in range(2, int(math.sqrt(p)) + 1)):
            return p

def compute_minimal_order_of_gqr(cnf, p):
    gqr_set = set()
    for clause in cnf:
        for literal in clause:
            if literal < 0:
                continue
            gqr_set.add(literal**2 % p)
    return len(gqr_set)

def resolution_width(cnf):
    # Simplified DPLL solver to estimate resolution width
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clauses = [c for c in clauses if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0][0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                return True
            return False
        pure_literals = [l for l in range(1, max(cnf) + 1) if (all(l not in c for c in clauses) or all(-l not in c for c in clauses))]
        if pure_literals:
            literal = pure_literals[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                return True
            return False
        return False

    def simplify(clauses, assignment):
        new_clauses = []
        for clause in clauses:
            new_clause = [l for l in clause if l not in assignment or assignment[l]]
            if new_clause:
                new_clauses.append(new_clause)
        return new_clauses

    simplified_clauses = cnf
    while True:
        simplified_clauses = simplify(simplified_clauses, {})
        if dpll(simplified_clauses, {}):
            break
        else:
            for clause in simplified_clauses:
                if len(clause) == 2 and clause[0] != -clause[1]:
                    new_clause = [l for l in cnf if l != clause]
                    if not dpll(new_clause, {}):
                        return len(clause)
    return 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_random_cnf(n)
        p = generate_random_prime(n)
        min_order_gqr = compute_minimal_order_of_gqr(cnf, p)
        width = resolution_width(cnf)
        
        if min_order_gqr == 0 or width == 0:
            continue
        
        results.append({
            "n": n,
            "min_order_gqr": min_order_gqr,
            "width": width
        })
    
    if not results:
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean = sum(result["width"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["width"] - mean) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if abs(result["min_order_gqr"] / result["width"]) <= 1.5) / len(results)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": mean,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" not in r or r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if "conjecture_holds" not in r or r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")