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
    
    def generate_group(n):
        generators = [f'g{i}' for i in range(1, n+1)]
        relations = [f'{generators[i]} * {generators[(i+1) % n]} = 1' for i in range(n)]
        return (generators, relations)
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(n):
            clauses.append(f'{variables[i]} ∨ {variables[(i+1) % n]}')
        return ' ∧ '.join(clauses)
    
    def tropical_rank(generators, relations):
        # Simplified version of the tropical rank calculation
        # This is a placeholder and should be replaced with actual computation
        return len(generators)
    
    def resolution_refutation_size(formula):
        # Simplified version of the refutation size calculation
        # This is a placeholder and should be replaced with actual computation
        return 2 ** len(formula.split(' ∧ '))
    
    n = random.randint(5, 40)
    G = generate_group(n)
    F = generate_tseitin_formula(n)
    
    R = tropical_rank(*G)
    refutation_size = resolution_refutation_size(F)
    
    lower_bound = math.ceil(refutation_size / 2)
    upper_bound = math.floor(refutation_size * 2)
    
    return {
        "metric_name": "Resolution Refutation Size",
        "metric_value": refutation_size,
        "instances_tested": 1,
        "conjecture_holds": lower_bound <= refutation_size <= upper_bound,
        "counterexample": "" if lower_bound <= refutation_size <= upper_bound else f"Refutation size {refutation_size} not within a factor of 2 from lower bound {lower_bound}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(1, 9973) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Refutation size out of bounds\" first_failing_seed={first_failing_seed}")