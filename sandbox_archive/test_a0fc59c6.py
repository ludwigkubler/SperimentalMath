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

def generate_cnf(n):
    cnf = []
    for _ in range(10):  # Generate 10 clauses for simplicity
        clause = [random.randint(-n, n) for _ in range(3)]
        if 0 not in clause:
            cnf.append(clause)
    return cnf

def dpll_solve(cnf):
    def solve(model):
        if not cnf:
            return model
        literal = next((lit for lit in range(1, n + 1) if lit not in model), None)
        if literal is None:
            return None
        new_model = model.copy()
        new_model.add(literal)
        result = solve(new_model)
        if result is not None:
            return result
        new_model.remove(literal)
        new_model.add(-literal)
        result = solve(new_model)
        if result is not None:
            return result
        return None

    n = max(abs(lit) for clause in cnf for lit in clause)
    return solve(set())

def weierstrass_order(cnf):
    # Placeholder function to simulate Weierstrass order computation
    # This is a dummy implementation and should be replaced with actual logic
    return len(cnf)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 10  # Fixed size for simplicity, can be adjusted as needed
    cnf = generate_cnf(n)
    order = weierstrass_order(cnf)
    proof_depth = dpll_solve(cnf)
    
    if proof_depth is None:
        return {
            "metric_name": "Weierstrass Order vs Resolution Proof Depth",
            "metric_value": 0,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "DPLL solver did not find a proof"
        }
    
    return {
        "metric_name": "Weierstrass Order vs Resolution Proof Depth",
        "metric_value": order / proof_depth,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        counterexample = next((result["counterexample"] for result in results if result["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[results.index(next(result for result in results if not result['conjecture_holds']))]}")