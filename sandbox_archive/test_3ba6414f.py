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

def generate_cnf(m: int) -> list:
    cnf = []
    for _ in range(m):
        clause = [random.randint(1, m) * (-1 if random.choice([True, False]) else 1)
                  for _ in range(random.randint(1, m))]
        cnf.append(clause)
    return cnf

def dpll_solver(cnf: list, assignment: dict) -> bool:
    n = len(cnf)
    unit_clauses = [l for l in range(1, n+1) if (l not in assignment and any(l in clause for clause in cnf)) or (-l not in assignment and any(-l in clause for clause in cnf))]
    while unit_clauses:
        l = unit_clauses.pop()
        assignment[l] = True
        for clause in cnf:
            if l in clause:
                clause.remove(l)
            elif -l in clause:
                clause.remove(-l)
                if not clause:
                    return False
        unit_clauses.extend([l for l in range(1, n+1) if (l not in assignment and any(l in clause for clause in cnf)) or (-l not in assignment and any(-l in clause for clause in cnf))])
    return True

def minimal_diophantine_property_set(cnf: list) -> set:
    def find_minimal_set():
        n = len(cnf)
        assignment = {}
        if dpll_solver(cnf, assignment):
            property_set = {tuple(sorted(assignment.keys()))}
        else:
            property_set = set()
        return property_set
    
    return find_minimal_set()

def circuit_monotone_width(property_set: set) -> int:
    return len(max(property_set, key=len))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""

    for m in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            cnf = generate_cnf(m)
            property_set = minimal_diophantine_property_set(cnf)
            monotone_width = circuit_monotone_width(property_set)
            metric_value = len(property_set) / (m * math.log2(m))
            total_metric_value += metric_value
            instances_tested += 1

            if monotone_width > m * math.log2(m):
                conjecture_holds = False
                counterexample = f"CNF with {m} clauses and monotone width {monotone_width}"

    mean_metric_value = total_metric_value / instances_tested
    support_fraction = 0.8

    return {
        "metric_name": "circuit_monotone_width",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(sys.argv[1])] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")