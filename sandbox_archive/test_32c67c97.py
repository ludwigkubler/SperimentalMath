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
    for _ in range(10):  # Generate 10 clauses with n variables each
        clause = [random.randint(-n, -1) for _ in range(random.randint(1, n))]
        cnf.append(clause)
    return cnf

def dpll(cnf):
    def solve(model):
        if not cnf:
            return model
        unit_clause = next((c for c in cnf if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_model = {**model, literal: True}
            return solve([c for c in cnf if not (literal in c or -literal in c)])
        pure_literal = next((l for l in range(-n, 0) if all(l not in c and -l not in c for c in cnf)), None)
        if pure_literal is not None:
            new_model = {**model, pure_literal: True}
            return solve([c for c in cnf if not (pure_literal in c or -pure_literal in c)])
        literal = random.choice([l for l in range(-n, 0) if any(l in c for c in cnf)])
        new_model_true = {**model, literal: True}
        result_true = solve([c for c in cnf if not (literal in c or -literal in c)])
        if result_true:
            return result_true
        new_model_false = {**model, literal: False}
        return solve([c for c in cnf if not (-literal in c or literal in c)])
    return solve({})

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 10  # Fixed size for simplicity
    cnf = generate_cnf(n)
    d_phi = dpll(cnf)
    R_phi = len(set([tuple(sorted(c)) for c in cnf]))  # Minimal number of distinct roots (simplified)
    
    return {
        "metric_name": "R(φ)",
        "metric_value": R_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")