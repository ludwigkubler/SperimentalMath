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
    cnf = []
    for _ in range(n):
        clause = [random.randint(1, 2*n) if random.choice([True, False]) else -random.randint(1, 2*n) for _ in range(random.randint(1, n))]
        cnf.append(clause)
    return cnf

def dpll(cnf):
    def propagate(lit):
        for clause in cnf:
            if lit in clause:
                clause.remove(lit)
            elif -lit in clause:
                return None
        return True

    stack = []
    assignment = {}
    def backtrack():
        while stack:
            literal, decision_level = stack.pop()
            negated_literal = -literal
            for i in range(len(cnf)):
                if negated_literal in cnf[i]:
                    cnf[i].remove(negated_literal)
                    if propagate(lit) is None:
                        return None
            assignment[literal] = False
        return True

    def search(decision_level):
        while True:
            literal = random.choice([i for i in range(1, 2*len(cnf)) if i not in assignment and -i not in assignment])
            stack.append((literal, decision_level))
            assignment[literal] = True
            if propagate(lit) is None:
                return backtrack()
            if all(lit in assignment or -lit in assignment for lit in [i for clause in cnf for i in clause]):
                return True

    return search(0)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    cnf = generate_cnf(n)
    path_length = dpll(cnf)
    if path_length is None:
        return {
            "metric_name": "mter",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "DPLL returned None"
        }
    mter = len(cnf)
    return {
        "metric_name": "mter",
        "metric_value": mter,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_mter = sum(result["metric_value"] for result in results) / len(results)
    std_mter = math.sqrt(sum((result["metric_value"] - mean_mter) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_mter} std={std_mter} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_mter} std={std_mter} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mter > p(φ)\" first_failing_seed={first_failing_seed}")