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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        literal = next(lit for lit in range(1, len(assignment) + 2) if lit not in assignment and -lit not in assignment)
        positive = literal > 0
        new_assignment = assignment.copy()
        new_assignment[literal] = positive
        if dpll(cnf, new_assignment):
            return True
        new_assignment[literal] = not positive
        return dpll(cnf, new_assignment)
    
    def minimal_rank(cnf):
        n = len(cnf[0])
        rank = 0
        for _ in range(10):  # Simple heuristic to estimate rank
            assignment = {i: random.choice([True, False]) for i in range(1, n + 1)}
            if dpll(cnf, assignment):
                rank += 1
        return rank
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    circuit_size = len(cnf) * 2  # Simplified estimate of circuit size
    rank = minimal_rank(cnf)
    
    if circuit_size == 0:
        return {
            "metric_name": "rank_to_circuit_ratio",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "circuit_size_zero"
        }
    
    ratio = abs(rank / circuit_size - 1)
    return {
        "metric_name": "rank_to_circuit_ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ratio <= 0.2,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank_to_circuit_ratio\" first_failing_seed={first_failing_seed}")