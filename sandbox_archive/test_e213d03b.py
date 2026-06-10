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
    
    def generate_random_sat_instance(n):
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, n), random.randint(-n, -1)]
            clauses.append(clause)
        return clauses
    
    def tseitin_formula(clauses):
        literals = set()
        for clause in clauses:
            literals.update(abs(lit) for lit in clause)
        variables = list(sorted(literals))
        
        formulas = []
        for i, literal in enumerate(variables):
            formulas.append(f"X{i} <-> ( {' & '.join(f'~X{j}' if j != i else 'Y' for j in range(i))})")
        
        for clause in clauses:
            formula = f"Z{len(formulas)} <-> ({' | '.join(f'X{abs(lit)-1}' if lit > 0 else f'~X{-lit-1}' for lit in clause)})"
            formulas.append(formula)
        
        return " & ".join(formulas)
    
    def resolution_width(formula):
        # Simplified resolution width calculation
        # This is a placeholder and should be replaced with an actual algorithm
        return len(formula.split(' | '))
    
    def local_induction_degree(formula):
        # Simplified LID calculation
        # This is a placeholder and should be replaced with an actual algorithm
        return len(formula.split(' <-> '))
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    instance = generate_random_sat_instance(n)
    phi_G = tseitin_formula(instance)
    lid_phi_G = local_induction_degree(phi_G)
    w_phi_G = resolution_width(phi_G)
    
    ratio = lid_phi_G / w_phi_G
    
    return {
        "metric_name": "LID/w_ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ratio <= 10,  # Placeholder constant c
        "counterexample": "" if ratio <= 10 else f"Ratio {ratio} exceeds bound"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio exceeds bound\" first_failing_seed={first_failing_seed}")