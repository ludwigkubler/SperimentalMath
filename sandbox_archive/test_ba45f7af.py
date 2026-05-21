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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    clause_indicator_poly = compute_clause_indicator_poly(cnf)
    schur_vanishing_count = count_schur_vanishing(clause_indicator_poly)
    acc0_circuit_size = estimate_acc0_circuit_size(cnf)
    
    metric_name = "schur_vanishing_count"
    metric_value = schur_vanishing_count
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""
    
    if acc0_circuit_size is not None:
        conjecture_holds = schur_vanishing_count == O(polylog(n))
        if not conjecture_holds:
            counterexample = f"Schur vanishing count {schur_vanishing_count} does not match ACC^0 circuit size bound {acc0_circuit_size}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def generate_cnf(n: int) -> list:
    cnf = []
    for _ in range(random.randint(1, n)):
        clause = random.sample(range(n), random.randint(1, n))
        cnf.append(clause)
    return cnf

def compute_clause_indicator_poly(cnf: list) -> dict:
    poly = {}
    for clause in cnf:
        term = 1
        for var in clause:
            term *= (1 + x**var)
        poly[tuple(sorted(clause))] = term
    return poly

def count_schur_vanishing(poly: dict) -> int:
    vanishing_count = 0
    for key, value in poly.items():
        if value == 0:
            vanishing_count += 1
    return vanishing_count

def estimate_acc0_circuit_size(cnf: list) -> int:
    # Placeholder function to estimate ACC^0 circuit size
    # This is a dummy implementation and should be replaced with actual logic
    return random.randint(1, 10)

def O(polylog_n):
    # Placeholder for the O(polylog(n)) bound
    # This is a dummy implementation and should be replaced with actual logic
    return polylog_n

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")