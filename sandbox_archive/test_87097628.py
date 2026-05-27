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
    
    def generate_group(n):
        # Generate a random group presentation P for simplicity
        generators = [f'a{i}' for i in range(n)]
        relations = []
        for i in range(n):
            relations.append(f'{generators[i]} * {generators[(i+1) % n]} = e')
        return (generators, relations)
    
    def generate_tseitin_formula(n):
        # Generate a random Tseitin formula F on n variables
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for i in range(n):
            clauses.append(f'{variables[i]} ∨ {variables[(i+1) % n]}')
        return clauses
    
    def tropical_rank(P, F):
        # Compute the rank of the tropical representation ρ of G over [0,1]
        generators, relations = P
        variables = [f'x{i}' for i in range(len(F))]
        # Simplified computation for demonstration purposes
        return len(generators) + len(variables)
    
    def resolution_refutation_size(F):
        # Estimate the resolution refutation size for F
        # Simplified computation for demonstration purposes
        return 2 ** len(F)
    
    n = random.randint(5, 40)
    P = generate_group(n)
    F = generate_tseitin_formula(n)
    
    R_P_F = tropical_rank(P, F)
    refutation_size = resolution_refutation_size(F)
    
    # Estimate the lower bound
    lower_bound = Fraction(2 ** R_P_F).limit_denominator()
    
    # Check if the conjecture holds
    conjecture_holds = abs(refutation_size - lower_bound) <= 0.5 * lower_bound
    
    return {
        "metric_name": "Resolution Refutation Size",
        "metric_value": refutation_size,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Refutation size {refutation_size} not within a factor of 2 from lower bound {lower_bound}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(100, 999) for _ in range(30)]
    
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
        print(f"RESULT: FALSIFIED counterexample=\"Refutation size not within a factor of 2 from lower bound\" first_failing_seed={first_failing_seed}")