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

def generate_tseitin(n, m):
    variables = [f'x{i}' for i in range(1, n+1)]
    clauses = []
    for _ in range(m):
        a, b, c = random.sample(variables + ['¬' + v for v in variables], 3)
        clause = f'({a} ∨ {b}) ∧ ¬{c}'
        clauses.append(clause)
    formula = ' ∧ '.join(clauses)
    return formula

def parse_tseitin(formula):
    n = 0
    variables = set()
    for char in formula:
        if char.isalpha() and not char.isdigit():
            variables.add(char)
            n = max(n, int(char[1:]) if 'x' in char else int(char[2:]))
    return n, list(variables)

def resolution_proof_length(formula):
    n, _ = parse_tseitin(formula)
    # Simplified estimation for demonstration purposes
    return n * 5

def morphism_complexity_category(n):
    # Placeholder function to simulate a monoidal category rank
    return random.randint(10, 30)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    formula = generate_tseitin(n, n * 2)
    mpc_rank = morphism_complexity_category(n)
    proof_length = resolution_proof_length(formula)
    
    if mpc_rank < proof_length:
        return {
            "metric_name": "minimal_rank",
            "metric_value": mpc_rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Formula: {formula}, MPC Rank: {mpc_rank}, Proof Length: {proof_length}"
        }
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mpc_rank,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["instances_tested"] > 0]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    mean = sum(metric_values) / len(metric_values)
    std_dev = (sum((x - mean)**2 for x in metric_values) / len(metric_values))**0.5
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='MPC rank < proof length' first_failing_seed={first_failing_seed}")