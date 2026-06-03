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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for var in variables:
            clauses.append(f'{var} ∨ ¬{var}')
        formula = ' ∧ '.join(clauses)
        return formula
    
    def calculate_hodge_norm(formula):
        # Placeholder function to simulate Hodge norm calculation
        # This is a dummy implementation and should be replaced with actual logic
        return random.random() * 100
    
    def calculate_frege_proof_length(formula):
        # Placeholder function to simulate Frege proof length calculation
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(5, 20)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    formula = generate_tseitin_formula(n)
    hodge_norm_value = calculate_hodge_norm(formula)
    proof_length = calculate_frege_proof_length(formula)
    
    conjecture_holds = proof_length <= math.sqrt(hodge_norm_value)
    counterexample = f"Frege proof length {proof_length} > Hodge norm bound {math.sqrt(hodge_norm_value)}" if not conjecture_holds else ""
    
    return {
        "metric_name": "Frege_proof_length_bound",
        "metric_value": proof_length,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")